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
                ("company_ids", "child_of", self.env.company.id),
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
                ("company_ids", "child_of", self.env.company.id),
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
                "l10n_it_account_stamp_stamp_duty_apply_tax_ids": [
                    (6, 0, [self.tax_id.id])
                ],
                "property_account_income_id": account_revenue_id.id,
                "property_account_expense_id": account_expense_id.id,
            }
        )
        self.env.company.l10n_it_account_stamp_stamp_duty_product_id = stamp_product_id

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
        self.assertTrue(invoice.l10n_it_account_stamp_is_stamp_duty_applied)
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
        invoice.button_draft()
        invoice.add_stamp_duty_invoice_line()
        self.assertEqual(invoice.invoice_line_ids[0].name, edited_descr)

    def test_amount_total_changing_currency(self):
        """Modify invoice currency and check that amount_total does not change after
        action_post"""
        stamp_duty_product = (
            self.env.company.l10n_it_account_stamp_stamp_duty_product_id
        )
        stamp_duty_product.l10n_it_account_stamp_auto_compute = False
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )
        invoice_form = Form(invoice)
        invoice_form.l10n_it_account_stamp_manually_apply_stamp_duty = False
        invoice_form.currency_id = self.env.ref("base.USD")
        invoice = invoice_form.save()
        total = invoice.amount_total
        invoice.action_post()
        self.assertEqual(total, invoice.amount_total)

    def test_reset_invoice_to_draft(self):
        """Reset an invoice to draft and check that relative tax stamp accounting lines
        has been deleted."""
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )

        self.assertEqual(len(invoice), 1)
        self.assertEqual(len(invoice.invoice_line_ids), 2)

        invoice.invoice_line_ids[0].write({"tax_ids": [(6, 0, [self.tax_id.id])]})
        invoice.action_post()

        self.assertEqual(
            len(invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 2
        )

        invoice.button_draft()

        self.assertEqual(
            len(invoice.line_ids.filtered(lambda line: line.is_stamp_line)), 0
        )

    def test_compute_l10n_it_stamp_duty(self):
        """Test that l10n_it_stamp_duty is correctly computed based on stamp
        application and product price."""
        stamp_product = self.env.company.l10n_it_account_stamp_stamp_duty_product_id
        stamp_price = stamp_product.list_price

        # Test 1: Invoice in draft with stamp duty applied
        invoice = first(
            self.invoices.filtered(lambda inv: inv.move_type == "out_invoice")
        )
        invoice.invoice_line_ids[0].write({"tax_ids": [(6, 0, [self.tax_id.id])]})
        self.assertTrue(invoice.l10n_it_account_stamp_is_stamp_duty_applied)
        self.assertEqual(invoice.state, "draft")
        self.assertEqual(
            invoice.l10n_it_stamp_duty,
            stamp_price,
            "Stamp duty should equal product price when applied in draft",
        )

        # Test 2: Invoice in draft without stamp duty applied
        invoice2 = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": "2024-01-01",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Product Without Stamp",
                            "price_unit": 100.0,
                            "quantity": 1,
                        },
                    )
                ],
            }
        )
        self.assertFalse(invoice2.l10n_it_account_stamp_is_stamp_duty_applied)
        self.assertEqual(invoice2.state, "draft")
        self.assertEqual(
            invoice2.l10n_it_stamp_duty,
            0,
            "Stamp duty should be 0 when not applied",
        )

        # Test 3: Posted invoice should keep value from draft
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertEqual(
            invoice.l10n_it_stamp_duty,
            stamp_price,
            "Stamp duty should be preserved after posting",
        )

        # Test 4: Change stamp product price and verify recomputation
        new_price = 5.0
        stamp_product.list_price = new_price
        invoice3 = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner_a.id,
                "invoice_date": "2024-01-01",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Product",
                            "price_unit": 100.0,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.tax_id.id])],
                        },
                    )
                ],
            }
        )
        self.assertTrue(invoice3.l10n_it_account_stamp_is_stamp_duty_applied)
        self.assertEqual(
            invoice3.l10n_it_stamp_duty,
            new_price,
            "Stamp duty should reflect updated product price",
        )
