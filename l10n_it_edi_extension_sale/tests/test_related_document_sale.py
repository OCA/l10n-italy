# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestItEdiSaleRelatedDocuments(TestItEdi):
    def _create_order(self, product_uom_qty=1):
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
                    "product_uom_qty": product_uom_qty,
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

    @staticmethod
    def _get_documents_data(documents):
        """Comparable representation of related documents.

        Documents are copied from the order to the invoice,
        so they cannot be compared by identity.
        """
        return {(document.type, document.name) for document in documents}

    def assertSameDocuments(self, documents, other_documents):
        self.assertEqual(
            self._get_documents_data(documents),
            self._get_documents_data(other_documents),
        )

    def test_create_invoice(self):
        """
        Generate an invoice from a sale order.
        Check that related documents are copied
        from the sale order (and its lines) to the invoice (and its lines).
        """
        order_line, sale_order = self._create_order()

        # Check the invoice
        invoice = sale_order._create_invoices()
        self.assertEqual(len(invoice), 1, "Multiple invoices for sale order")
        self.assertSameDocuments(
            sale_order.related_document_ids, invoice.related_document_ids
        )
        # The documents are copied: the order keeps its own
        self.assertFalse(sale_order.related_document_ids & invoice.related_document_ids)
        self.assertEqual(sale_order.related_document_ids.sale_order_id, sale_order)
        self.assertFalse(invoice.related_document_ids.sale_order_id)

        # Check the invoice line
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda line, ol=order_line: ol <= line.sale_line_ids
        )
        self.assertEqual(
            len(invoice_line), 1, "Multiple invoice lines for sale order line"
        )
        self.assertSameDocuments(
            order_line.related_document_ids, invoice_line.related_document_ids
        )
        self.assertFalse(
            order_line.related_document_ids & invoice_line.related_document_ids
        )
        self.assertEqual(
            invoice_line.l10n_it_edi_admin_ref, order_line.l10n_it_edi_admin_ref
        )

    def test_create_invoice_multiple(self):
        """
        Generate a grouping invoice from multiple orders.
        Check that related documents are copied
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
        self.assertEqual(len(invoice.related_document_ids), 2)
        self.assertSameDocuments(
            sale_orders.related_document_ids, invoice.related_document_ids
        )

        # Check the invoice lines
        self.assertEqual(len(invoice.invoice_line_ids.related_document_ids), 2)
        self.assertSameDocuments(
            sale_orders_lines.related_document_ids,
            invoice.invoice_line_ids.related_document_ids,
        )

    def test_create_invoice_partial(self):
        """
        Invoice a sale order in two steps.
        Check that each invoice (and its lines) gets its own copy
        of the related documents of the sale order (and its lines).
        """
        self.product_a.invoice_policy = "delivery"
        order_line, sale_order = self._create_order(product_uom_qty=2)

        first_invoice = sale_order._create_invoices()
        self.assertEqual(len(first_invoice), 1, "Multiple invoices for sale order")

        order_line.qty_delivered = 2
        second_invoice = sale_order._create_invoices()
        self.assertEqual(len(second_invoice), 1, "Multiple invoices for sale order")
        self.assertNotEqual(first_invoice, second_invoice)

        for invoice in first_invoice | second_invoice:
            self.assertSameDocuments(
                sale_order.related_document_ids, invoice.related_document_ids
            )
            self.assertSameDocuments(
                order_line.related_document_ids,
                invoice.invoice_line_ids.related_document_ids,
            )
        # Every invoice has its own documents
        self.assertFalse(
            first_invoice.related_document_ids & second_invoice.related_document_ids
        )
        self.assertFalse(
            first_invoice.invoice_line_ids.related_document_ids
            & second_invoice.invoice_line_ids.related_document_ids
        )

    def test_keep_document(self):
        """
        Delete an invoice having related documents copied from a sale order.
        Check that the related documents of the sale order are kept.
        """
        order_line, sale_order = self._create_order()
        order_documents = (
            sale_order.related_document_ids | order_line.related_document_ids
        )

        invoice = sale_order._create_invoices()
        self.assertEqual(len(invoice), 1, "Multiple invoices for sale order")
        invoice_documents = (
            invoice.related_document_ids | invoice.invoice_line_ids.related_document_ids
        )
        self.assertEqual(len(invoice_documents), 2)

        # Delete the invoice: the documents of the invoice are deleted,
        # the documents of the sale order persist
        invoice.unlink()
        self.assertFalse(invoice_documents.exists())
        self.assertEqual(order_documents.exists(), order_documents)

        # Delete the sale order: its documents are deleted too
        sale_order._action_cancel()
        sale_order.unlink()
        self.assertFalse(order_documents.exists())
