from odoo.tests import Form, tagged

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

    def test_keep_lines_description(self):
        """Check that description is kept in other lines when adding stamp."""
        # Get an invoice and make it eligible for applying stamp
        invoice = self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        self.assertEqual(len(invoice), 1)
        invoice.invoice_line_ids[0].write({"tax_ids": [(6, 0, [self.tax_id.id])]})

        # Edit the description of first line
        invoice_form = Form(invoice)
        edited_descr = "Test edited description"
        with invoice_form.invoice_line_ids.edit(0) as line:
            line.name = edited_descr
        invoice = invoice_form.save()
        invoice.action_post()

        # Add stamp and check that edited description is kept
        invoice.add_tax_stamp_line()
        self.assertEqual(invoice.invoice_line_ids[0].name, edited_descr)

    def test_amount_total_changing_currency(self):
        """Modify invoice currency and check that amount_total does not change after
        action_post"""
        self.env.company.tax_stamp_product_id.auto_compute = False
        invoice = self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        invoice_form = Form(invoice)
        invoice_form.manually_apply_tax_stamp = False
        invoice_form.currency_id = self.env.ref("base.USD")
        invoice = invoice_form.save()
        total = invoice.amount_total
        invoice.action_post()
        self.assertEqual(total, invoice.amount_total)
