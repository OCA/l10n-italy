from odoo.fields import first
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
                    "account_type",
                    "=",
                    "income",
                ),
            ],
            limit=1,
        )
        account_expense_id = self.env["account.account"].search(
            [
                ("company_id", "=", self.env.company.id),
                (
                    "account_type",
                    "=",
                    "expense",
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
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )

        self.assertEqual(len(invoice), 1)
        self.assertEqual(len(invoice.invoice_line_ids), 2)

        invoice.invoice_line_ids[0].write({"tax_ids": [(6, 0, [self.tax_id.id])]})
        self.assertEqual(
            len(invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 0
        )
        self.assertTrue(invoice.tax_stamp)
        invoice.action_post()

        self.assertEqual(
            len(invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 2
        )

    def test_keep_lines_description(self):
        """Check that description is kept in other lines when adding stamp."""
        # Get an invoice and make it eligible for applying stamp
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )
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
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )
        invoice_form = Form(invoice)
        invoice_form.manually_apply_tax_stamp = False
        invoice_form.currency_id = self.env.ref("base.USD")
        invoice = invoice_form.save()
        total = invoice.amount_total
        invoice.action_post()
        self.assertEqual(total, invoice.amount_total)
