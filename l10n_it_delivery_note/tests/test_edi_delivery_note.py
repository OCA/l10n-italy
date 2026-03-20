# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from lxml import etree

from odoo.tests import Form, tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


@tagged("post_install", "-at_install")
class TestEdiDeliveryNote(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env.user.groups_id |= cls.env.ref(
            "sales_team.group_sale_salesman"
        ) | cls.env.ref("stock.group_stock_manager")

        cls.products = (
            cls.env["product.product"]
            .with_company(cls.company)
            .create(
                [
                    {
                        # The name is the Descrizione of the exported line
                        "name": f"Test product {number}",
                        "type": "consu",
                        "is_storable": False,
                        "list_price": 100.0 * number,
                        "invoice_policy": "delivery",
                        "taxes_id": [(6, 0, cls.default_tax.ids)],
                    }
                    for number in (1, 2, 3)
                ]
            )
        )

    def _create_sale_order(self, lines):
        """Confirm a sale order for `lines`, a list of (product, quantity)."""
        sale_order = (
            self.env["sale.order"]
            .with_company(self.company)
            .create(
                {
                    "partner_id": self.italian_partner_a.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "product_uom_qty": quantity,
                                "price_unit": product.list_price,
                                "tax_id": [(6, 0, self.default_tax.ids)],
                            },
                        )
                        for product, quantity in lines
                    ],
                }
            )
        )
        sale_order.action_confirm()
        return sale_order

    def _validate_picking(self, picking, quantities=None):
        """Deliver `quantities`, a {product: quantity}, leaving a backorder."""
        for move in picking.move_ids:
            move.quantity = (
                move.product_uom_qty
                if quantities is None
                else quantities.get(move.product_id, 0.0)
            )
        action = picking.button_validate()
        if isinstance(action, dict) and action.get("res_model"):
            Form(
                self.env[action["res_model"]].with_context(**action["context"])
            ).save().process()
        self.assertEqual(picking.state, "done")
        return picking

    def _create_delivery_note(self, picking):
        self.env["stock.delivery.note.create.wizard"].with_context(
            active_model="stock.picking",
            active_ids=picking.ids,
        ).create({"partner_shipping_id": self.italian_partner_a.id}).confirm()
        delivery_note = picking.delivery_note_id
        self.assertTrue(delivery_note)
        delivery_note.action_confirm()
        return delivery_note

    def _create_deferred_invoice(self, delivery_notes):
        """Invoice `delivery_notes` together, the day after the shipping."""
        self.env["stock.delivery.note.invoice.wizard"].with_context(
            active_model="stock.delivery.note",
            active_ids=delivery_notes.ids,
        ).create({}).create_invoices()

        invoice = delivery_notes.invoice_ids
        self.assertEqual(len(invoice), 1)
        self.assertEqual(invoice.delivery_note_ids, delivery_notes)
        invoice.invoice_date = max(delivery_notes.mapped("date")) + timedelta(days=1)
        return invoice

    def _get_exported_dati_ddt(self, invoice):
        """Get the exported DatiDDT as (NumeroDDT, DataDDT, [line description]).

        Every RiferimentoNumeroLinea is resolved to the description of the
        DettaglioLinee it points to, that is what it has to reference.
        """
        invoice_xml = etree.fromstring(invoice._l10n_it_edi_render_xml())
        descriptions = {
            line.findtext("NumeroLinea"): line.findtext("Descrizione")
            for line in invoice_xml.xpath("//DettaglioLinee")
        }
        exported_dati_ddt = []
        for exported_ddt in invoice_xml.xpath("//DatiDDT"):
            references = exported_ddt.xpath("RiferimentoNumeroLinea")
            self.assertFalse(
                {reference.text for reference in references} - set(descriptions),
                "The references must point to exported lines",
            )
            exported_dati_ddt.append(
                (
                    exported_ddt.findtext("NumeroDDT"),
                    exported_ddt.findtext("DataDDT"),
                    sorted(descriptions[reference.text] for reference in references),
                )
            )
        return exported_dati_ddt

    def _get_exported_document_type(self, invoice):
        invoice_xml = etree.fromstring(invoice._l10n_it_edi_render_xml())
        return invoice_xml.findtext(
            "FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/TipoDocumento"
        )

    def test_single_delivery_note(self):
        """One DdT is exported without line references."""
        product = self.products[0]
        sale_order = self._create_sale_order([(product, 5)])
        picking = self._validate_picking(sale_order.picking_ids)
        delivery_note = self._create_delivery_note(picking)
        invoice = self._create_deferred_invoice(delivery_note)
        invoice.action_post()

        self.assertEqual(
            self._get_exported_dati_ddt(invoice),
            [(delivery_note.name, str(delivery_note.date), [])],
        )
        self.assertEqual(self._get_exported_document_type(invoice), "TD24")

    def test_multiple_delivery_notes(self):
        """Every DdT is exported with the lines it ships.

        The first DdT ships the whole second product and half of the first one,
        the second DdT ships the whole third product and the other half:
        the invoice line of the first product belongs to both DdT.
        """
        product_a, product_b, product_c = self.products
        sale_order = self._create_sale_order(
            [(product_a, 10), (product_b, 5), (product_c, 5)]
        )
        first_picking = self._validate_picking(
            sale_order.picking_ids,
            {product_a: 5, product_b: 5, product_c: 0},
        )
        first_delivery_note = self._create_delivery_note(first_picking)
        second_picking = self._validate_picking(sale_order.picking_ids - first_picking)
        second_delivery_note = self._create_delivery_note(second_picking)

        invoice = self._create_deferred_invoice(
            first_delivery_note | second_delivery_note
        )
        invoice.action_post()
        self.assertEqual(
            len(invoice.invoice_line_ids.filtered(lambda line: line.product_id)), 3
        )

        self.assertEqual(
            self._get_exported_dati_ddt(invoice),
            [
                (
                    first_delivery_note.name,
                    str(first_delivery_note.date),
                    sorted([product_a.name, product_b.name]),
                ),
                (
                    second_delivery_note.name,
                    str(second_delivery_note.date),
                    sorted([product_a.name, product_c.name]),
                ),
            ],
        )
        self.assertEqual(self._get_exported_document_type(invoice), "TD24")

    def test_multiple_delivery_notes_reordered_lines(self):
        """The line references follow the exported lines.

        The DettaglioLinee are not numbered after the sequence of the
        invoice lines, so the references cannot be counted on it.
        """
        product_a, product_b = self.products[0], self.products[1]
        sale_order = self._create_sale_order([(product_a, 5), (product_b, 5)])
        first_picking = self._validate_picking(
            sale_order.picking_ids, {product_a: 5, product_b: 0}
        )
        first_delivery_note = self._create_delivery_note(first_picking)
        second_picking = self._validate_picking(sale_order.picking_ids - first_picking)
        second_delivery_note = self._create_delivery_note(second_picking)

        invoice = self._create_deferred_invoice(
            first_delivery_note | second_delivery_note
        )
        # Display the lines in the reverse order of the exported one
        invoice_lines = invoice.invoice_line_ids.filtered(lambda line: line.product_id)
        for sequence, invoice_line in enumerate(reversed(invoice_lines)):
            invoice_line.sequence = sequence
        invoice.action_post()

        self.assertEqual(
            self._get_exported_dati_ddt(invoice),
            [
                (
                    first_delivery_note.name,
                    str(first_delivery_note.date),
                    [product_a.name],
                ),
                (
                    second_delivery_note.name,
                    str(second_delivery_note.date),
                    [product_b.name],
                ),
            ],
        )

    def test_draft_delivery_note_not_exported(self):
        """A DdT without number and date is not exported."""
        product = self.products[0]
        sale_order = self._create_sale_order([(product, 5)])
        picking = self._validate_picking(sale_order.picking_ids)
        delivery_note = self._create_delivery_note(picking)
        invoice = self._create_deferred_invoice(delivery_note)
        invoice.action_post()

        draft_delivery_note = (
            self.env["stock.delivery.note"]
            .with_company(self.company)
            .create(
                {
                    "partner_sender_id": self.company.partner_id.id,
                    "partner_id": self.italian_partner_a.id,
                    "partner_shipping_id": self.italian_partner_a.id,
                }
            )
        )
        self.assertFalse(draft_delivery_note.name)
        invoice.delivery_note_ids |= draft_delivery_note

        self.assertEqual(
            self._get_exported_dati_ddt(invoice),
            [(delivery_note.name, str(delivery_note.date), [])],
        )
