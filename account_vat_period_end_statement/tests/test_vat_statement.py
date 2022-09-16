#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.rrule import MONTHLY

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
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
                [("account_type", "=", "asset_current")],
                limit=1,
            )
            .id
        )
        cls.received_vat_account = (
            cls.env["account.account"]
            .search(
                [("account_type", "=", "liability_current")],
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
                "code": "VAT.AUTH",
                "name": "VAT Authority",
                "reconcile": True,
                "account_type": "liability_payable",
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
                        "account_type",
                        "=",
                        "income",
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
        self.account_tax_22.invalidate_model()
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

    def _create_vendor_bill(self, partner, invoice_date, price_unit, tax):
        """
        Create an open Vendor Bill for `partner` having date `invoice_date`.
        The Bill will also have a Line having Price `price_unit` and Tax `tax`.
        """
        bill_model = self.invoice_model.with_context(default_move_type="in_invoice")
        bill_form = Form(bill_model)
        bill_form.partner_id = partner
        bill_form.invoice_date = invoice_date
        with bill_form.invoice_line_ids.new() as line:
            line.tax_ids.clear()
            line.tax_ids.add(tax)
            line.name = "Test Invoice Line"
            line.account_id = self.company_data["default_account_expense"]
            line.price_unit = price_unit
        bill = bill_form.save()
        bill.action_post()
        return bill

    def _get_statement(self, period, statement_date, accounts):
        """
        Create a VAT Statement in date `statement_date`
        for Period `period` and Accounts `accounts`.
        """
        # Create statement
        statement_form = Form(self.vat_statement_model)
        statement_form.journal_id = self.general_journal
        statement_form.authority_vat_account_id = self.vat_authority
        statement_form.payment_term_id = self.account_payment_term
        statement_form.date = statement_date
        statement_form.account_ids.clear()
        for account in accounts:
            statement_form.account_ids.add(account)
        statement = statement_form.save()

        # Add period
        add_period_model = self.env["add.period.to.vat.statement"]
        add_period_model = add_period_model.with_context(
            active_id=statement.id,
            active_model=statement._name,
        )
        add_period_form = Form(add_period_model)
        add_period_form.period_id = period
        add_period = add_period_form.save()
        add_period.add_period()
        return statement

    def test_different_previous_vat_statements(self):
        """
        Statements for different Accounts
        only count previous Amounts from Statements with the same Accounts.
        """
        # Arrange: Create two different VAT Statements
        # selecting two different Accounts
        partner = self.env.ref("base.res_partner_4")
        tax = self.account_tax_22_credit
        tax_statement_account = tax.vat_statement_account_id
        last_year_bill = self._create_vendor_bill(
            partner,
            self.last_year_recent_date,
            10,
            tax,
        )
        self.assertEqual(last_year_bill.state, "posted")
        last_year_period = self.last_year_period
        last_year_statement = self._get_statement(
            last_year_period,
            self.last_year_date,
            tax_statement_account,
        )
        self.assertTrue(last_year_statement)

        # Create another Bill and Statement
        other_tax_statement_account = tax_statement_account.copy()
        other_tax = tax.copy(
            default={
                "vat_statement_account_id": other_tax_statement_account.id,
            },
        )
        other_last_year_bill = self._create_vendor_bill(
            partner,
            self.last_year_recent_date,
            20,
            other_tax,
        )
        self.assertEqual(other_last_year_bill.state, "posted")
        last_year_period.type_id.allow_overlap = True
        other_last_year_period = last_year_period.copy(
            default={
                "name": "Test Other last Year Period",
                "vat_statement_id": False,
            },
        )
        other_last_year_statement = self._get_statement(
            other_last_year_period,
            self.last_year_date,
            other_tax_statement_account,
        )
        self.assertTrue(other_last_year_statement)

        # Act: Create this Year's Statements,
        # one for each Account used in previous Statements
        today = fields.Date.today()
        current_period = self.current_period
        statement = self._get_statement(
            current_period,
            today,
            tax_statement_account,
        )

        current_period.type_id.allow_overlap = True
        other_current_period = current_period.copy(
            default={
                "name": "Test Other current Period",
                "vat_statement_id": False,
            },
        )
        other_statement = self._get_statement(
            other_current_period,
            today,
            other_tax_statement_account,
        )

        # Assert: Each one of this Year's Statements counts as previous Amount
        # only the corresponding last Year's Statement
        self.assertEqual(
            statement.previous_credit_vat_amount,
            -last_year_statement.authority_vat_amount,
        )
        self.assertEqual(
            other_statement.previous_credit_vat_amount,
            -other_last_year_statement.authority_vat_amount,
        )
