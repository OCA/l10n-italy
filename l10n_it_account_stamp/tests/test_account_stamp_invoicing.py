from odoo.tests import tagged

from odoo.addons.account.tests.test_account_invoice_report import (
    TestAccountInvoiceReport,
)


@tagged("post_install", "-at_install")
class InvoicingTest(TestAccountInvoiceReport):
    def setUp(self):
        super().setUp()
        tax_model = self.env["account.tax"]
        self.tax_id = tax_model.create({"name": "Art. 15", "amount": 0})
        stamp_product_id = self.env.ref(
            "l10n_it_account_stamp.l10n_it_account_stamp_2_euro"
        )

        account_revenue_id = self.env["account.account"].search(
            [
                ("company_id", "=", self.env.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                ),
            ],
            limit=1,
        )
        account_expense_id = self.env["account.account"].search(
            [
                ("company_id", "=", self.env.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
            ],
            limit=1,
        )
        stamp_product_id.write(
            {
                "stamp_apply_tax_ids": [(6, 0, [self.tax_id.id])],
                "property_account_income_id": account_revenue_id.id,
                "property_account_expense_id": account_expense_id.id,
            }
        )
        self.env.company.tax_stamp_product_id = stamp_product_id

    def test_post_invoicing(self):
        invoice_ids = self.invoices.filtered(
            lambda invoice: invoice.move_type == "out_invoice"
        )

        self.assertEqual(len(invoice_ids), 1)
        final_invoice = invoice_ids[0]
        self.assertEqual(len(final_invoice.invoice_line_ids), 2)

        final_invoice.invoice_line_ids[0].write({"tax_ids": [(6, 0, [self.tax_id.id])]})
        self.assertEqual(
            len(final_invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 0
        )
        self.assertTrue(final_invoice.tax_stamp)
        final_invoice.action_post()

        self.assertEqual(
            len(final_invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 2
        )
