# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.l10n_it_edi.tests.common import TestItEdi
from odoo.addons.l10n_it_edi_extension_sale import _post_init_hook


class TestPostInitHook(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.order = cls._create_order()
        cls.invoice = cls.order._create_invoices()
        # Tables and columns of the legacy `l10n_it_fatturapa_sale` module
        cls.env.cr.execute(
            """
            CREATE TABLE IF NOT EXISTS fatturapa_related_document_type (
                id SERIAL PRIMARY KEY,
                type CHARACTER VARYING,
                name CHARACTER VARYING,
                "lineRef" INTEGER,
                invoice_id INTEGER,
                invoice_line_id INTEGER,
                date DATE,
                numitem CHARACTER VARYING,
                code CHARACTER VARYING,
                cig CHARACTER VARYING,
                cup CHARACTER VARYING,
                sale_order_id INTEGER,
                sale_order_line_id INTEGER
            )
            """
        )
        cls.env.cr.execute(
            """
            ALTER TABLE sale_order_line
            ADD COLUMN IF NOT EXISTS admin_ref CHARACTER VARYING
            """
        )

    @classmethod
    def _create_order(cls):
        order = cls.env["sale.order"].create(
            {
                "partner_id": cls.italian_partner_a.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product_a.id,
                            "product_uom_qty": 1,
                        }
                    )
                ],
            }
        )
        order.action_confirm()
        return order

    def _create_legacy_document(self, vals, **legacy_vals):
        """Create a document as copied from the legacy table by
        `l10n_it_edi_related_document`, and its row in the legacy table.
        """
        document = self.env["account.move.related_document"].create(vals)
        self._create_legacy_row(**legacy_vals)
        return document

    def _create_legacy_row(self, **legacy_vals):
        columns = ", ".join(legacy_vals)
        values = ", ".join("%s" for __ in legacy_vals)
        self.env.cr.execute(
            f"""
            INSERT INTO fatturapa_related_document_type ({columns})
            VALUES ({values})
            """,
            tuple(legacy_vals.values()),
        )

    def _run_hook(self):
        _post_init_hook(self.env)
        self.env.invalidate_all()

    def test_recover_sale_order_document(self):
        """A document attached to a sale order only is linked back to it."""
        document = self._create_legacy_document(
            {"type": "order", "name": "order1"},
            type="order",
            name="order1",
            sale_order_id=self.order.id,
        )
        self._run_hook()
        self.assertEqual(document.sale_order_id, self.order)
        self.assertFalse(document.invoice_id)
        # Running the hook again does not change anything
        self._run_hook()
        self.assertEqual(document.sale_order_id, self.order)

    def test_recover_sale_order_line_document(self):
        """A document attached to a sale order line only is linked back."""
        order_line = self.order.order_line
        document = self._create_legacy_document(
            {"type": "reception", "name": "line1"},
            type="reception",
            name="line1",
            sale_order_line_id=order_line.id,
        )
        self._run_hook()
        self.assertEqual(document.sale_order_line_id, order_line)
        self.assertFalse(document.invoice_line_id)

    def test_recover_invoiced_document(self):
        """An invoiced document is copied to the sale order."""
        invoice_document = self._create_legacy_document(
            {"type": "order", "name": "order2", "invoice_id": self.invoice.id},
            type="order",
            name="order2",
            invoice_id=self.invoice.id,
            sale_order_id=self.order.id,
        )
        self._run_hook()
        # The document of the invoice is not changed
        self.assertEqual(invoice_document.invoice_id, self.invoice)
        self.assertFalse(invoice_document.sale_order_id)
        # The sale order gets its own copy of the document
        order_document = self.order.related_document_ids
        self.assertEqual(len(order_document), 1)
        self.assertNotEqual(order_document, invoice_document)
        self.assertEqual(order_document.type, "order")
        self.assertEqual(order_document.name, "order2")
        self.assertFalse(order_document.invoice_id)
        # Running the hook again does not copy the document twice
        self._run_hook()
        self.assertEqual(self.order.related_document_ids, order_document)

    def test_recover_ambiguous_document(self):
        """A document related to different sale orders is left unlinked."""
        document = self._create_legacy_document(
            {"type": "order", "name": "order3"},
            type="order",
            name="order3",
            sale_order_id=self.order.id,
        )
        self._create_legacy_row(
            type="order",
            name="order3",
            sale_order_id=self._create_order().id,
        )
        self._run_hook()
        self.assertFalse(document.sale_order_id)

    def test_no_legacy_table(self):
        """Installing the module on a clean database does nothing."""
        self.env.cr.execute("DROP TABLE fatturapa_related_document_type")
        self._run_hook()

    def test_recover_admin_ref(self):
        """The Admin. Ref. of the sale order lines is recovered."""
        order_line = self.order.order_line
        self.env.cr.execute(
            "UPDATE sale_order_line SET admin_ref = %s WHERE id = %s",
            ("1" * 23, order_line.id),
        )
        self._run_hook()
        # The new field is 20 characters wide
        self.assertEqual(order_line.l10n_it_edi_admin_ref, "1" * 20)
