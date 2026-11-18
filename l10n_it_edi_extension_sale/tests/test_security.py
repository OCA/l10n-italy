# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests import new_test_user

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


class TestRelatedDocumentSecurity(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesman = new_test_user(
            cls.env,
            login="related_document_salesman",
            groups="base.group_user,sales_team.group_sale_salesman",
        )
        # A user who can read the invoices, but not change them
        cls.readonly_salesman = new_test_user(
            cls.env,
            login="related_document_readonly_salesman",
            groups=(
                "base.group_user,"
                "sales_team.group_sale_salesman,"
                "account.group_account_readonly"
            ),
        )
        # A user who can change the invoices
        cls.accounting_salesman = new_test_user(
            cls.env,
            login="related_document_accounting_salesman",
            groups=(
                "base.group_user,"
                "sales_team.group_sale_salesman,"
                "account.group_account_invoice"
            ),
        )
        cls.order = cls._create_order()
        cls.invoice = cls.order._create_invoices()
        # The document related to the order line is copied to the invoice
        # line: changing it does not write on the invoice.
        cls.invoice_line_document = cls.invoice.invoice_line_ids.related_document_ids
        # The document related to the invoice is not the standard related
        # document of the invoice, so changing it does not write on it.
        cls.invoice.write(
            {
                "related_document_ids": [
                    Command.create({"type": "reception", "name": "reception2"})
                ]
            }
        )
        cls.invoice_document = cls.invoice.related_document_ids
        cls.invoice.action_post()

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
                            "related_document_ids": [
                                Command.create(
                                    {"type": "reception", "name": "reception1"}
                                )
                            ],
                        }
                    )
                ],
            }
        )
        order.action_confirm()
        return order

    def test_change_order_line_document(self):
        """A salesman can change the documents of a sale order line."""
        document = self.order.order_line.related_document_ids
        document.with_user(self.salesman).write({"name": "changed"})
        self.assertEqual(document.name, "changed")

    def test_change_draft_invoice_document(self):
        """A salesman can change the documents of a draft invoice."""
        invoice = self._create_order()._create_invoices()
        self.assertEqual(invoice.state, "draft")
        document = invoice.invoice_line_ids.related_document_ids
        document.with_user(self.salesman).write({"name": "changed"})
        self.assertEqual(document.name, "changed")

    def test_change_posted_invoice_line_document(self):
        """A salesman cannot change a document of a posted invoice line."""
        self.assertEqual(self.invoice.state, "posted")
        # The document is readable for the salesman
        self.invoice_line_document.with_user(self.salesman).read(["name"])
        with self.assertRaises(AccessError):
            self.invoice_line_document.with_user(self.salesman).write(
                {"name": "changed"}
            )
        self.assertEqual(self.invoice_line_document.name, "reception1")

    def test_change_posted_invoice_document(self):
        """A salesman cannot change a document of a posted invoice."""
        self.assertEqual(self.invoice.state, "posted")
        self.invoice_document.with_user(self.readonly_salesman).read(["name"])
        with self.assertRaises(AccessError):
            self.invoice_document.with_user(self.readonly_salesman).write(
                {"name": "changed"}
            )
        self.assertEqual(self.invoice_document.name, "reception2")

    def test_change_posted_invoice_document_accounting(self):
        """An accounting user can change a document of a posted invoice."""
        self.assertEqual(self.invoice.state, "posted")
        self.invoice_document.with_user(self.accounting_salesman).write(
            {"name": "changed"}
        )
        self.assertEqual(self.invoice_document.name, "changed")

    def test_create_posted_invoice_document(self):
        """A salesman cannot add a document to a posted invoice."""
        self.assertEqual(self.invoice.state, "posted")
        with self.assertRaises(AccessError):
            self.env["account.move.related_document"].with_user(self.salesman).create(
                {
                    "type": "reception",
                    "name": "reception3",
                    "invoice_line_id": self.invoice.invoice_line_ids.id,
                }
            )

    def test_unlink_posted_invoice_document(self):
        """A salesman cannot delete a document of a posted invoice."""
        self.assertEqual(self.invoice.state, "posted")
        with self.assertRaises(AccessError):
            self.invoice_line_document.with_user(self.salesman).unlink()
        self.assertTrue(self.invoice_line_document.exists())
