# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestItEdiSaleRelatedDocuments(TestItEdi):
    def _create_order(self):
        sale_order = (
            self.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": self.italian_partner_a.id,
                    "related_document_ids": [
                        Command.create({"type": "order", "name": "order1"})
                    ],
                }
            )
        )
        order_line = (
            self.env["sale.order.line"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "order_id": sale_order.id,
                    "product_id": self.product_a.id,
                    "product_uom_qty": 1,
                    "qty_delivered": 1,
                    "l10n_it_edi_admin_ref": "line admin ref",
                    "related_document_ids": [
                        Command.create({"type": "order", "name": "line1"})
                    ],
                }
            )
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
        self.assertTrue(sale_order.related_document_ids <= invoice.related_document_ids)

        # Check the invoice line
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda line, ol=order_line: ol <= line.sale_line_ids
        )
        self.assertEqual(
            len(invoice_line), 1, "Multiple invoice lines for sale order line"
        )

        self.assertTrue(
            order_line.related_document_ids <= invoice_line.related_document_ids
        )
        self.assertEqual(
            invoice_line.l10n_it_edi_admin_ref, order_line.l10n_it_edi_admin_ref
        )

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
        self.assertTrue(
            sale_orders.mapped("related_document_ids") <= invoice.related_document_ids
        )

        # Check the invoice lines
        self.assertEqual(
            invoice.invoice_line_ids.mapped("related_document_ids"),
            sale_orders_lines.mapped("related_document_ids"),
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
        related_documents = invoice.related_document_ids

        # Delete the invoice: the related document persists
        invoice.unlink()
        self.assertTrue(related_documents.exists())

        # Delete the sale order: the related document is deleted too
        sale_order._action_cancel()
        sale_order.unlink()
        self.assertFalse(related_documents.exists())
