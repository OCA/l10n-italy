#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.rrule import MONTHLY

from odoo.tests.common import TransactionCase


class TestTax(TransactionCase):
    def setUp(self):
        super(TestTax, self).setUp()
        self.range_type = self.env["date.range.type"].create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        generator = self.env["date.range.generator"]
        generator = generator.create(
            {
                "date_start": "%s-01-01" % datetime.now().year,
                "name_prefix": "%s-" % datetime.now().year,
                "type_id": self.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        generator.action_apply()
        prev_year_generator = generator.create(
            {
                "date_start": "%s-01-01" % (datetime.now().year - 1),
                "name_prefix": "%s-" % (datetime.now().year - 1),
                "type_id": self.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        prev_year_generator.action_apply()
        self.tax_model = self.env["account.tax"]
        self.account_model = self.env["account.account"]
        self.term_model = self.env["account.payment.term"]
        self.term_line_model = self.env["account.payment.term.line"]
        self.invoice_model = self.env["account.move"]
        self.invoice_line_model = self.env["account.move.line"]
        today = datetime.now().date()
        self.current_period = self.env["date.range"].search(
            [("date_start", "<=", today), ("date_end", ">=", today)]
        )
        self.last_year_date = date(today.year - 1, today.month, today.day)
        self.last_year_period = self.env["date.range"].search(
            [
                ("date_start", "<=", self.last_year_date),
                ("date_end", ">=", self.last_year_date),
            ]
        )
        self.vat_statement_model = self.env["account.vat.period.end.statement"]
        self.paid_vat_account = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        self.received_vat_account = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref(
                            "account.data_account_type_current_liabilities"
                        ).id,
                    )
                ],
                limit=1,
            )
            .id
        )

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        self.recent_date = (
            self.invoice_model.search(
                [("invoice_date", "!=", False)], order="invoice_date desc", limit=1
            ).invoice_date
            or today
        )
        self.last_year_recent_date = date(
            self.recent_date.year - 1, self.recent_date.month, self.recent_date.day
        )

        self.account_tax_22 = self.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": self.received_vat_account,
                "type_tax_use": "sale",
            }
        )
        self.account_tax_22_credit = self.tax_model.create(
            {
                "name": "22% credit",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": self.paid_vat_account,
                "type_tax_use": "purchase",
            }
        )

        self.vat_authority = self.account_model.create(
            {
                "code": "VAT AUTH",
                "name": "VAT Authority",
                "reconcile": True,
                "user_type_id": self.env.ref("account.data_account_type_payable").id,
            }
        )

        self.account_payment_term = self.term_model.create(
            {
                "name": "16 Days End of Month",
                "note": "16 Days End of Month",
            }
        )
        self.term_line_model.create(
            {
                "value": "balance",
                "days": 16,
                "option": "after_invoice_month",
                "payment_id": self.account_payment_term.id,
            }
        )
        self.sale_journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        self.purchase_journal = self.env["account.journal"].search(
            [("type", "=", "purchase")], limit=1
        )
        self.general_journal = self.env["account.journal"].search(
            [("type", "=", "general")], limit=1
        )

    def test_vat_statement(self):
        in_invoice_line_account = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_revenue").id,
                    )
                ],
                limit=1,
            )
            .id
        )

        out_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.sale_journal.id,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 100,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22.id])],
                        },
                    )
                ],
            }
        )
        out_invoice._recompute_tax_lines()
        out_invoice.action_post()

        in_invoice = self.invoice_model.create(
            {
                "invoice_date": self.recent_date,
                "journal_id": self.purchase_journal.id,
                "partner_id": self.env.ref("base.res_partner_4").id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": in_invoice_line_account,
                            "price_unit": 50,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22_credit.id])],
                        },
                    )
                ],
            }
        )
        in_invoice._recompute_tax_lines()
        in_invoice.action_post()

        last_year_in_invoice = self.invoice_model.create(
            {
                "invoice_date": self.last_year_recent_date,
                "journal_id": self.purchase_journal.id,
                "partner_id": self.env.ref("base.res_partner_4").id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "price_unit": 50,
                            "quantity": 1,
                            "tax_ids": [(6, 0, [self.account_tax_22_credit.id])],
                        },
                    )
                ],
            }
        )
        last_year_in_invoice._recompute_tax_lines()
        last_year_in_invoice.action_post()

        self.last_year_vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
                "date": self.last_year_date,
            }
        )
        self.last_year_period.vat_statement_id = self.last_year_vat_statement
        self.last_year_vat_statement.compute_amounts()

        self.vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
            }
        )
        self.current_period.vat_statement_id = self.vat_statement
        self.account_tax_22.refresh()
        self.vat_statement.compute_amounts()
        self.vat_statement._compute_authority_vat_amount()
        self.vat_statement.previous_credit_vat_account_id = self.received_vat_account

        self.assertEqual(self.vat_statement.previous_credit_vat_amount, 11)
        self.assertTrue(self.vat_statement.previous_year_credit)
        self.assertEqual(self.vat_statement.authority_vat_amount, 0)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 11)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(len(self.vat_statement.debit_vat_account_line_ids), 1)
        self.assertEqual(len(self.vat_statement.credit_vat_account_line_ids), 1)
        self.vat_statement.advance_account_id = self.paid_vat_account
        self.vat_statement.advance_amount = 100
        self.vat_statement._compute_authority_vat_amount()
        self.assertEqual(self.vat_statement.authority_vat_amount, -100)
        self.vat_statement.create_move()
        self.assertEqual(self.vat_statement.state, "confirmed")
        self.assertTrue(self.vat_statement.move_id)
        vat_auth_found = False
        for line in self.vat_statement.move_id.line_ids:
            if line.account_id.id == self.vat_statement.authority_vat_account_id.id:
                vat_auth_found = True
                self.assertEqual(line.debit, 100)
        self.assertTrue(vat_auth_found)
        # TODO payment
