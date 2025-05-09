#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2022 Simone Rubino - TAKOBI
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.rrule import MONTHLY

from odoo.tests import Form

from odoo.addons.l10n_it_edi.tests.test_edi_reverse_charge import TestItEdiReverseCharge


class TestVATStatementCommon(TestItEdiReverseCharge):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.range_type = cls.env["date.range.type"].create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        generator = cls.env["date.range.generator"]
        current_datetime = datetime(2020, month=6, day=15)
        previous_datetime = datetime(2019, month=6, day=15)
        generator = generator.create(
            {
                "date_start": f"{current_datetime:%Y}-01-01",
                "name_prefix": f"{current_datetime:%Y}-",
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        generator.action_apply()
        prev_year_generator = generator.create(
            {
                "date_start": f"{previous_datetime:%Y}-01-01",
                "name_prefix": f"{previous_datetime:%Y}-",
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        prev_year_generator.action_apply()
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
        cls.paid_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    ("account_type", "=", "asset_current"),
                    ("company_ids", "in", cls.company.id),
                ],
                limit=1,
            )
            .id
        )
        cls.received_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    ("account_type", "=", "liability_current"),
                    ("company_ids", "in", cls.company.id),
                ],
                limit=1,
            )
            .id
        )

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        cls.recent_date = (
            cls.env["account.move"]
            .search(
                [("invoice_date", "!=", False), ("company_id", "=", cls.company.id)],
                order="invoice_date desc",
                limit=1,
            )
            .invoice_date
            or current_date
        )
        cls.last_year_recent_date = date(
            cls.recent_date.year - 1, cls.recent_date.month, cls.recent_date.day
        )

        cls.vat_authority = cls.env["account.account"].create(
            {
                "code": "VAT.AUTH",
                "name": "VAT Authority",
                "reconcile": True,
                "account_type": "liability_payable",
                "company_ids": [(6, 0, [cls.company.id])],
            }
        )

        cls.account_payment_term = cls.env["account.payment.term"].create(
            {
                "name": "16 Days End of Month",
                "note": "16 Days End of Month",
                "company_id": cls.company.id,
            }
        )
        cls.env["account.payment.term.line"].create(
            {
                "value": "percent",
                "value_amount": 100,
                "nb_days": 16,
                "payment_id": cls.account_payment_term.id,
            }
        )

    def _create_vendor_bill(self, partner, invoice_date, price_unit, tax):
        """
        Create an open Vendor Bill for `partner` having date `invoice_date`.
        The Bill will also have a Line having Price `price_unit` and Tax `tax`.
        """
        bill_model = self.env["account.move"].with_context(
            default_move_type="in_invoice"
        )
        bill_form = Form(bill_model)
        bill_form.partner_id = partner
        bill_form.invoice_date = invoice_date
        with bill_form.invoice_line_ids.new() as line:
            line.tax_ids.clear()
            line.tax_ids.add(tax)
            line.name = "Test Invoice Line"
            line.account_id = self.company_data_2["default_account_expense"]
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
        statement_form = Form(self.env["account.vat.period.end.statement"])
        statement_form.journal_id = self.company_data_2["default_journal_misc"]
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
