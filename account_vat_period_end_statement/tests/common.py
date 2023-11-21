#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2022 Simone Rubino - TAKOBI
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.rrule import MONTHLY

from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestVATStatementCommon(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.range_type = cls.env["date.range.type"].create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        generator = cls.env["date.range.generator"]
        current_datetime = datetime(2020, month=6, day=15)
        generator = generator.create(
            {
                "date_start": "%s-01-01" % current_datetime.year,
                "name_prefix": "%s-" % current_datetime.year,
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        generator.action_apply()
        prev_year_generator = generator.create(
            {
                "date_start": "%s-01-01" % (current_datetime.year - 1),
                "name_prefix": "%s-" % (current_datetime.year - 1),
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
        current_date = current_datetime.date()
        cls.current_period = cls.env["date.range"].search(
            [("date_start", "<=", current_date), ("date_end", ">=", current_date)]
        )
        cls.last_year_date = date(
            current_date.year - 1, current_date.month, current_date.day
        )
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
            or current_date
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

    def _get_statement(self, period, statement_date, accounts, payment_term=None):
        """
        Create a VAT Statement in date `statement_date`
        for Period `period` and Accounts `accounts`.
        """
        if payment_term is None:
            payment_term = self.account_payment_term
        # Create statement
        statement_form = Form(self.vat_statement_model)
        statement_form.journal_id = self.general_journal
        statement_form.authority_vat_account_id = self.vat_authority
        statement_form.payment_term_id = payment_term
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
