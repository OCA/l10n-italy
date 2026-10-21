from lxml import etree

from odoo import Command

from odoo.addons.l10n_it_edi.tests.common import TestItEdi

RELATED_DOCUMENT_TAGS = [
    "DatiOrdineAcquisto",
    "DatiContratto",
    "DatiConvenzione",
    "DatiRicezione",
    "DatiFattureCollegate",
]


class TestItEdiExport(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.french_partner = cls.env["res.partner"].create(
            {
                "name": "Alessi",
                "vat": "FR15437982937",
                "country_id": cls.env.ref("base.fr").id,
                "street": "Avenue Test rue",
                "zip": "84000",
                "city": "Avignon",
                "is_company": True,
            }
        )
        cls.purchase_rc_tax = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "22% purchase Reverse Charge",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                    "invoice_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("03", "vj9")),
                        cls.RepartitionLine(100, "tax", ("5v",)),
                        cls.RepartitionLine(-100, "tax", ("4v",)),
                    ),
                    "refund_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100, "base", ("03", "vj9")),
                        cls.RepartitionLine(100, "tax", False),
                        cls.RepartitionLine(-100, "tax", False),
                    ),
                }
            )
        )

    def _create_invoice(self, **values):
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.write({"invoice_date_due": invoice.invoice_date, **values})
        return invoice

    def _get_related_document_nodes(self, invoice):
        """Return tag and IdDocumento of the related documents in the XML,
        in the order they are exported."""
        tree = etree.fromstring(invoice._l10n_it_edi_render_xml())
        return [
            (node.tag, node.findtext("IdDocumento"))
            for node in tree.xpath("//DatiGenerali/*")
            if node.tag in RELATED_DOCUMENT_TAGS
        ]

    def test_export_reference(self):
        """The related documents are exported after the purchase order
        that core exports for the reference of the invoice."""
        invoice = self._create_invoice(
            ref="PO-CUSTOMER",
            related_document_ids=[
                Command.create({"type": "invoice", "name": "INV1"}),
                Command.create({"type": "contract", "name": "CONTRACT1"}),
                Command.create({"type": "order", "name": "ORDER1"}),
            ],
        )
        invoice.action_post()

        self.assertEqual(
            self._get_related_document_nodes(invoice),
            [
                ("DatiOrdineAcquisto", "PO-CUSTOMER"),
                ("DatiOrdineAcquisto", "ORDER1"),
                ("DatiContratto", "CONTRACT1"),
                ("DatiFattureCollegate", "INV1"),
            ],
        )

    def test_export_debit_note(self):
        """The related documents of a debit note are exported
        before the invoice that core exports for the debit note,
        as required by the FatturaPA schema."""
        origin = self._create_invoice()
        origin.action_post()
        debit_note = self._create_invoice(
            debit_origin_id=origin.id,
            ref="Price adjustment",
            related_document_ids=[
                Command.create({"type": "order", "name": "ORDER1"}),
            ],
        )
        debit_note.action_post()

        self.assertEqual(
            self._get_related_document_nodes(debit_note),
            [
                ("DatiOrdineAcquisto", "ORDER1"),
                ("DatiFattureCollegate", "Price adjustment"),
            ],
        )

    def test_export_self_invoice(self):
        """The related documents of a self-invoice are exported
        before the invoice that core exports for its reference,
        as required by the FatturaPA schema."""
        self_invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2022-03-24",
                    "invoice_date_due": "2022-03-24",
                    "date": "2022-04-01",
                    "partner_id": self.french_partner.id,
                    "ref": "FT00001",
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Product A",
                                "product_id": self.product_a.id,
                                "price_unit": 800.40,
                                "tax_ids": [Command.set(self.purchase_rc_tax.ids)],
                            }
                        ),
                    ],
                    "related_document_ids": [
                        Command.create({"type": "order", "name": "ORDER1"}),
                    ],
                }
            )
        )
        self_invoice.action_post()
        # pre-condition
        self.assertTrue(self_invoice.l10n_it_edi_is_self_invoice)

        self.assertEqual(
            self._get_related_document_nodes(self_invoice),
            [
                ("DatiOrdineAcquisto", "ORDER1"),
                ("DatiFattureCollegate", "FT00001"),
            ],
        )
