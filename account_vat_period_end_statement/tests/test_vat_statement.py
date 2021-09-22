#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.rrule import MONTHLY

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestTax(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.range_type = cls.env["date.range.type"].create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        generator = cls.env["date.range.generator"]
        generator = generator.create(
            {
                "date_start": "%s-01-01" % datetime.now().year,
                "name_prefix": "%s-" % datetime.now().year,
                "type_id": cls.range_type.id,
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
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        prev_year_generator.action_apply()
        cls.tax_model = cls.env["account.tax"]
        cls.account_model = cls.env["account.account"]
        cls.term_model = cls.env["account.payment.term"]
        cls.term_line_model = cls.env["account.payment.term.line"]
        cls.invoice_model = cls.env["account.move"]
        cls.invoice_line_model = cls.env["account.move.line"]
        today = datetime.now().date()
        cls.current_period = cls.env["date.range"].search(
            [("date_start", "<=", today), ("date_end", ">=", today)]
        )
        cls.last_year_date = date(today.year - 1, today.month, today.day)
        cls.last_year_period = cls.env["date.range"].search(
            [
                ("date_start", "<=", cls.last_year_date),
                ("date_end", ">=", cls.last_year_date),
            ]
        )
        cls.vat_statement_model = cls.env["account.vat.period.end.statement"]
        cls.paid_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        cls.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        cls.received_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        cls.env.ref("account.data_account_type_current_liabilities").id,
                    )
                ],
                limit=1,
            )
            .id
        )

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        cls.recent_date = (
            cls.invoice_model.search(
                [("invoice_date", "!=", False)], order="invoice_date desc", limit=1
            ).invoice_date
            or today
        )
        cls.last_year_recent_date = date(
            cls.recent_date.year - 1, cls.recent_date.month, cls.recent_date.day
        )
        cls.account_tax_22 = cls.company_data["default_tax_sale"].copy(
            {
                "name": "22%",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": cls.received_vat_account,
                "type_tax_use": "sale",
            }
        )
        cls.account_tax_22_credit = cls.company_data["default_tax_purchase"].copy(
            {
                "name": "22% credit",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": cls.paid_vat_account,
                "type_tax_use": "purchase",
            }
        )

        cls.vat_authority = cls.account_model.create(
            {
                "code": "VAT AUTH",
                "name": "VAT Authority",
                "reconcile": True,
                "user_type_id": cls.env.ref("account.data_account_type_payable").id,
            }
        )

        cls.account_payment_term = cls.term_model.create(
            {
                "name": "16 Days End of Month",
                "note": "16 Days End of Month",
            }
        )
        cls.term_line_model.create(
            {
                "value": "balance",
                "days": 16,
                "option": "after_invoice_month",
                "payment_id": cls.account_payment_term.id,
            }
        )
        cls.sale_journal = cls.company_data["default_journal_sale"]
        cls.purchase_journal = cls.company_data["default_journal_purchase"]
        cls.general_journal = cls.company_data["default_journal_misc"]

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
