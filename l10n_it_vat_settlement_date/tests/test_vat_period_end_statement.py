#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import tagged
from odoo.tools import formatLang

from odoo.addons.l10n_it_account_vat_period_end_settlement.tests.common import (
    TestVATStatementCommon,
)


@tagged("post_install", "-at_install")
class TestVATPeriodEndStatement(TestVATStatementCommon):
    def test_statement(self):
        """The settlement date decides whether a move is in the statement."""
        # Set the company context
        self.env.user.company_id = self.company.id
        # Arrange: a date range and a bill out of that range
        current_period = self.current_period
        tax = self.company_data_2["default_tax_purchase"]
        out_of_period_date = current_period.date_end + relativedelta(days=+1)
        bill = self._create_vendor_bill(
            self.env.ref("base.res_partner_4"),
            out_of_period_date,
            100,
            tax,
        )
        statement = self._get_statement(
            current_period,
            fields.Date.today(),
            [],
        )
        authority_vat_amount = statement.authority_vat_amount
        # pre-condition
        period_settled_moves = self.env["account.move"].search(
            current_period.get_domain("l10n_it_vat_settlement_date")
        )
        self.assertNotIn(bill, period_settled_moves)

        # Act: move the settlement date in the statement period
        bill.l10n_it_vat_settlement_date = current_period.date_end + relativedelta(
            days=-1
        )

        # Assert: the statement now contains the bill
        period_settled_moves = self.env["account.move"].search(
            current_period.get_domain("l10n_it_vat_settlement_date")
        )
        self.assertIn(bill, period_settled_moves)

        bill.line_ids.tax_ids.invalidate_recordset()
        statement.compute_amounts()
        new_authority_vat_amount = statement.authority_vat_amount
        self.assertNotEqual(
            authority_vat_amount,
            new_authority_vat_amount,
        )
        self.assertEqual(
            new_authority_vat_amount, authority_vat_amount + bill.amount_tax_signed
        )

    def _get_report(self, statement):
        """Print the Vat Period End Statement of `statement`."""
        report_action = self.env.ref(
            "l10n_it_account_vat_period_end_settlement.report_vat_statement"
        )
        html, _report_type = self.env["ir.actions.report"]._render_qweb_html(
            report_action.report_name, statement.ids
        )
        return html

    def test_report(self):
        """When the settlement date is out of period,
        the tax amounts are not shown in the report."""
        # Set the company context
        self.env.user.company_id = self.company.id
        # Arrange
        current_period = self.current_period
        tax = self.company_data_2["default_tax_purchase"]
        in_period_date = current_period.date_end + relativedelta(days=-1)
        bill = self._create_vendor_bill(
            self.env.ref("base.res_partner_4"),
            in_period_date,
            100,
            tax,
        )
        out_of_period_date = current_period.date_end + relativedelta(days=+1)
        bill.l10n_it_vat_settlement_date = out_of_period_date
        statement = self._get_statement(
            current_period,
            fields.Date.today(),
            [],
        )
        # pre-condition
        period_settled_moves = self.env["account.move"].search(
            current_period.get_domain("l10n_it_vat_settlement_date")
        )
        self.assertNotIn(bill, period_settled_moves)

        # Act
        # Invalidate the tax's cache otherwise the same (correct) values
        # computed by the statement are printed in the report
        tax.invalidate_recordset(
            fnames=[
                "deductible_balance",
            ],
        )
        report_content = self._get_report(statement)

        # Assert
        report_content = report_content.decode()
        self.assertNotIn(formatLang(statement.env, bill.amount_tax), report_content)
