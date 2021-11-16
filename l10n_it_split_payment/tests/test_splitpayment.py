# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2018  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.test_account_account import TestAccountAccount


@tagged("post_install", "-at_install")
class TestSP(TestAccountAccount):
    def setUp(self):
        super().setUp()
        self.tax_model = self.env["account.tax"]
        self.move_model = self.env["account.move"]
        self.term_model = self.env["account.payment.term"]
        self.move_line_model = self.env["account.move.line"]
        self.fp_model = self.env["account.fiscal.position"]
        self.account_model = self.env["account.account"]

        self.company = self.env.company
        self.tax22sp = self.tax_model.create(
            {
                "name": "22% SP",
                "amount": 22,
            }
        )
        self.tax22 = self.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
            }
        )
        self.sp_fp = self.fp_model.create(
            {
                "name": "Split payment",
                "split_payment": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {"tax_src_id": self.tax22.id, "tax_dest_id": self.tax22sp.id},
                    )
                ],
            }
        )
        self.company.sp_account_id = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_current_assets").id,
                )
            ],
            limit=1,
        )
        account_user_type = self.env.ref("account.data_account_type_receivable")
        self.a_recv = self.account_model.create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=account_user_type.id,
                reconcile=True,
            )
        )
        # set account receivable on partner
        partner_id = self.env.ref("base.res_partner_3")
        partner_id.property_account_receivable_id = self.a_recv.id
        self.a_sale = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        self.sales_journal = self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", self.company.id)]
        )[0]
        self.term_15_30 = self.term_model.create(
            {
                "name": "15 30",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "value_amount": 50,
                            "days": 15,
                            "sequence": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "days": 30,
                            "sequence": 2,
                        },
                    ),
                ],
            }
        )
        # Set invoice date to recent date in the system
        # This solves problems with account_invoice_sequential_dates
        self.recent_date = self.move_model.search(
            [("invoice_date", "!=", False)], order="invoice_date desc", limit=1
        ).invoice_date

    def test_invoice(self):
        self.assertTrue(self.tax22sp.is_split_payment)
        invoice = self.move_model.with_context(default_move_type="out_invoice").create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "journal_id": self.sales_journal.id,
                "fiscal_position_id": self.sp_fp.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": self.a_sale.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, {self.tax22sp.id})],
                        },
                    )
                ],
            }
        )
        self.assertTrue(invoice.split_payment)
        invoice.action_post()
        self.assertEqual(invoice.amount_sp, 22)
        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.amount_residual, 100)
        self.assertEqual(invoice.amount_tax, 0)
        vat_line = False
        credit_line = False
        for line in invoice.line_ids:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.debit, 22)
            if line.account_id.id == self.a_recv.id:
                credit_line = True
                self.assertEqual(line.debit, 100)
        self.assertTrue(vat_line)
        self.assertTrue(credit_line)
        invoice.button_draft()
        invoice.button_cancel()

        invoice2 = self.move_model.with_context(default_move_type="out_invoice").create(
            {
                "partner_id": self.env.ref("base.res_partner_3").id,
                "journal_id": self.sales_journal.id,
                "fiscal_position_id": self.sp_fp.id,
                "invoice_payment_term_id": self.term_15_30.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": self.a_sale.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, {self.tax22sp.id})],
                        },
                    )
                ],
            }
        )
        invoice2.action_post()
        self.assertEqual(invoice2.amount_sp, 22)
        self.assertEqual(invoice2.amount_total, 100)
        self.assertEqual(invoice2.amount_residual, 100)
        self.assertEqual(invoice2.amount_tax, 0)
        vat_line = False
        credit_line_count = 0
        for line in invoice2.line_ids:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.debit, 22)
            if line.account_id.id == self.a_recv.id:
                credit_line_count += 1
                self.assertEqual(line.debit, 50)
        self.assertTrue(vat_line)
        self.assertEqual(credit_line_count, 2)

        # refund
        invoice3 = self.move_model.with_context(default_move_type="out_invoice").create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "journal_id": self.sales_journal.id,
                "fiscal_position_id": self.sp_fp.id,
                "move_type": "out_refund",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": self.a_sale.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, {self.tax22sp.id})],
                        },
                    )
                ],
            }
        )
        self.assertTrue(invoice3.split_payment)
        invoice3.action_post()
        self.assertEqual(invoice3.amount_sp, 22)
        self.assertEqual(invoice3.amount_total, 100)
        self.assertEqual(invoice3.amount_residual, 100)
        self.assertEqual(invoice3.amount_tax, 0)
        vat_line = False
        credit_line = False
        for line in invoice3.line_ids:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.credit, 22)
            if line.account_id.id == self.a_recv.id:
                credit_line = True
                self.assertEqual(line.credit, 100)
        self.assertTrue(vat_line)
        self.assertTrue(credit_line)

    def test_balanced_lines(self):
        self.assertTrue(self.tax22sp.is_split_payment)

        invoice_form = Form(
            self.move_model.with_context(default_move_type="out_invoice")
        )
        invoice_form.invoice_date = self.recent_date
        invoice_form.partner_id = self.env.ref("base.res_partner_3")
        invoice_form.journal_id = self.sales_journal
        invoice_form.fiscal_position_id = self.sp_fp

        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.name = "service"
            line_form.account_id = self.a_sale
            line_form.quantity = 1
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax22sp)

        invoice = invoice_form.save()
        self.assertTrue(invoice.split_payment)
        self.assertEqual(invoice.amount_sp, 22)
        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.amount_residual, 100)
        self.assertEqual(invoice.amount_tax, 0)

        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.name = "service"
            line_form.account_id = self.a_sale
            line_form.quantity = 1
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax22sp)

        invoice = invoice_form.save()
        self.assertTrue(invoice.split_payment)
        self.assertEqual(invoice.amount_sp, 44)
        self.assertEqual(invoice.amount_total, 200)
        self.assertEqual(invoice.amount_residual, 200)
        self.assertEqual(invoice.amount_tax, 0)
