# Copyright 2017 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestDocType(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.journalrec = cls.company_data["default_journal_misc"]

        cls.doc_type_model = cls.env["fiscal.document.type"]
        cls.TD01 = cls.doc_type_model.search([("code", "=", "TD01")], limit=1)
        cls.TD01.journal_ids = cls.journalrec
        cls.TD04 = cls.doc_type_model.search([("code", "=", "TD04")], limit=1)
        cls.inv_model = cls.env["account.move"]
        cls.partner3 = cls.env.ref("base.res_partner_3")
        cls.fp = cls.env["account.fiscal.position"].create(
            {
                "name": "FP",
                "fiscal_document_type_id": cls.TD01.id,
            }
        )

    def test_doc_type(self):
        invoice = self.inv_model.create({"partner_id": self.partner3.id})
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.create({"partner_id": self.partner3.id})
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)

    def test_doc_type_on_invoice_create(self):
        """Check document type on invoice create based invoice type."""
        revenue_account = self.company_data["default_account_revenue"]
        product = self.env.ref("product.product_product_5")
        invoice = self.inv_model.create(
            {
                "partner_id": self.partner3.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
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
                            "product_id": product.id,
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
                            "product_id": product.id,
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
