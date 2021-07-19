# Copyright 2017 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestDocType(TransactionCase):
    def setUp(self):
        super(TestDocType, self).setUp()
        self.journalrec = self.env["account.journal"].search(
            [("type", "=", "general")], limit=1
        )
        self.doc_type_model = self.env["fiscal.document.type"]
        self.TD01 = self.doc_type_model.search([("code", "=", "TD01")], limit=1)
        self.TD01.journal_ids = self.journalrec
        self.TD04 = self.doc_type_model.search([("code", "=", "TD04")], limit=1)
        self.inv_model = self.env["account.move"]
        self.partner3 = self.env.ref("base.res_partner_3")
        self.fp = self.env["account.fiscal.position"].create(
            {
                "name": "FP",
                "fiscal_document_type_id": self.TD01.id,
            }
        )

    def test_doc_type(self):
        invoice = self.inv_model.create({"partner_id": self.partner3.id})
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.create({"partner_id": self.partner3.id})
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)

    def test_doc_type_on_invoice_create(self):
        """Check document type on invoice create based invoice type."""
        revenue_account_type = self.env.ref("account.data_account_type_revenue")
        revenue_account = self.env["account.account"].search(
            [("user_type_id", "=", revenue_account_type.id)], limit=1
        )
        invoice = self.inv_model.create(
            {
                "partner_id": self.partner3.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref("product.product_product_5").id,
                            "quantity": 10.0,
                            "account_id": revenue_account.id,
                            "name": "product test 5",
                            "price_unit": 100.00,
                        },
                    )
                ],
            }
        )
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)

        invoice = self.inv_model.create(
            {
                "partner_id": self.partner3.id,
                "move_type": "out_refund",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref("product.product_product_5").id,
                            "quantity": 10.0,
                            "account_id": revenue_account.id,
                            "name": "product test 5",
                            "price_unit": 100.00,
                        },
                    )
                ],
            }
        )
        self.assertEqual(invoice.fiscal_document_type_id, self.TD04)

        invoice = self.inv_model.create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner3.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref("product.product_product_5").id,
                            "quantity": 10.0,
                            "account_id": revenue_account.id,
                            "name": "product test 5",
                            "price_unit": 100.00,
                        },
                    )
                ],
            }
        )
        invoice.action_post()

        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "reason": "no reason",
                    "refund_method": "cancel",
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        reverse_move = self.env["account.move"].browse(reversal["res_id"])
        self.assertEqual(reverse_move.move_type, "out_refund")
        self.assertEqual(reverse_move.fiscal_document_type_id.id, self.TD04.id)
