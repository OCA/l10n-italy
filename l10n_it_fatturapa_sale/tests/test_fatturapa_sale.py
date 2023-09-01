#  Copyright 2020 Simone Rubino - Agile Business Group
#  Copyright 2023 Sergio Corato <https://github.com/sergiocorato>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger
from odoo.tools.safe_eval import safe_eval


class TestFatturapaSale(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "invoice_policy": "order"}
        )
        cls.journal_model = cls.env["account.journal"]
        sale_journals = cls.journal_model.search([("type", "=", "sale")])
        for sale_journal in sale_journals:
            sale_journal.advance_fiscal_document_type_id = cls.env.ref(
                "l10n_it_fiscal_document_type.9"
            ).id

    def _create_order(self):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "related_documents": [(0, 0, {"type": "order", "name": "order1"})],
            }
        )
        order_line = self.env["sale.order.line"].create(
            {
                "order_id": sale_order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1,
                "qty_delivered": 1,
                "admin_ref": "line admin ref",
                "related_documents": [(0, 0, {"type": "order", "name": "line1"})],
            }
        )
        sale_order.action_confirm()
        return order_line, sale_order

    def test_create_invoice(self):
        """
        Generate an invoice from a sale order.
        Check that related documents are passed
        from the sale order (and its lines) to the invoice (and its lines).
        """
        order_line, sale_order = self._create_order()

        # Check the invoice
        invoice = sale_order._create_invoices()
        self.assertEqual(len(invoice), 1, "Multiple invoices for sale order")
        self.assertEqual(invoice.related_documents, sale_order.related_documents)

        # Check the invoice line
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda l: order_line in l.sale_line_ids
        )
        self.assertEqual(
            len(invoice_line), 1, "Multiple invoice lines for sale order line"
        )

        self.assertEqual(invoice_line.related_documents, order_line.related_documents)
        self.assertEqual(invoice_line.admin_ref, order_line.admin_ref)

    def test_create_invoice_multiple(self):
        """
        Generate a grouping invoice from multiple orders.
        Check that related documents are passed
        from the sale orders (and their lines)
        to the invoice (and its lines).
        """
        order_line1, sale_order1 = self._create_order()
        order_line2, sale_order2 = self._create_order()
        sale_orders = sale_order1 | sale_order2
        sale_orders_lines = order_line1 | order_line2

        # Check the invoice
        invoice = sale_orders._create_invoices()
        self.assertEqual(len(invoice), 1, "Multiple invoices for sale order")
        self.assertEqual(
            invoice.related_documents, sale_orders.mapped("related_documents")
        )

        # Check the invoice lines
        self.assertEqual(
            invoice.invoice_line_ids.mapped("related_documents"),
            sale_orders_lines.mapped("related_documents"),
        )

    def test_keep_document(self):
        """
        Delete an invoice having related documents.
        Check that the related documents are no more deleted
        if linked to a sale order.
        """
        order_line, sale_order = self._create_order()

        invoice = sale_order._create_invoices()
        self.assertEqual(len(invoice), 1, "Multiple invoices for sale order")
        related_documents = invoice.related_documents

        # Delete the invoice: the related document persists
        invoice.unlink()
        self.assertTrue(related_documents.exists())

        # Delete the sale order: the related document is deleted too
        sale_order.action_cancel()
        sale_order.unlink()
        self.assertFalse(related_documents.exists())

    @mute_logger("odoo.models", "odoo.models.unlink", "odoo.addons.base.ir.ir_model")
    def test_create_percentage_advance_invoice(self):
        order_line, sale_order = self._create_order()
        wizard_obj = self.env["sale.advance.payment.inv"]
        wizard_vals = wizard_obj.default_get(["advance_payment_method"])
        wizard_vals.update({"advance_payment_method": "percentage", "amount": 10.0})
        wizard = wizard_obj.with_context(
            active_ids=sale_order.ids, open_invoices=True
        ).create(wizard_vals)
        res = wizard.create_invoices()
        domain = safe_eval(res.get("domain"))
        domain.append(("id", "=", res["res_id"]))
        invoices = self.env[res["res_model"]].search(domain)
        self.assertTrue(len(invoices), 1)
        invoice = invoices[0]
        self.assertEqual(
            invoice.fiscal_document_type_id,
            invoice.journal_id.advance_fiscal_document_type_id,
        )

    @mute_logger("odoo.models", "odoo.models.unlink", "odoo.addons.base.ir.ir_model")
    def test_create_delivered_advance_invoice(self):
        order_line, sale_order = self._create_order()
        wizard_obj = self.env["sale.advance.payment.inv"]
        wizard_vals = wizard_obj.default_get(["advance_payment_method"])
        wizard_vals.update({"advance_payment_method": "delivered"})
        wizard = wizard_obj.with_context(
            active_ids=sale_order.ids, open_invoices=True
        ).create(wizard_vals)
        res = wizard.create_invoices()
        domain = safe_eval(res.get("domain"))
        domain.append(("id", "=", res["res_id"]))
        invoices = self.env[res["res_model"]].search(domain)
        self.assertTrue(len(invoices), 1)
        invoice = invoices[0]
        self.assertNotEqual(
            invoice.fiscal_document_type_id,
            invoice.journal_id.advance_fiscal_document_type_id,
        )
