# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

SECTION_ACCOUNT_TYPES_DICT = {
    # Assets = "Receivable", "Bank and Cash", "Current Assets",
    #          "Non-current Assets", "Fixed Assets", "Prepayments"
    "assets": [
        "asset_receivable",
        "asset_cash",
        "asset_current",
        "asset_non_current",
        "asset_fixed",
        "asset_prepayments",
    ],
    # Expenses = "Expenses", "Cost of Revenue", "Depreciation"
    "expenses": [
        "expense",
        "expense_direct_cost",
        "expense_depreciation",
    ],
    # Incomes = "Income", "Other Income"
    "incomes": [
        "income",
        "income_other",
    ],
    # Liabilities = "Current Year Earnings", "Payable", "Credit Card",
    #               "Current Liabilities", "Non-current Liabilities", "Equity"
    "liabilities": [
        "equity_unaffected",
        "liability_payable",
        "liability_credit_card",
        "liability_current",
        "liability_non_current",
        "equity",
    ],
}


class Account(models.Model):
    _inherit = "account.account"

    # This field is almost equal to `internal_group`; yet, we wanna keep the
    # report independent from Odoo's accounting workflow, so we'll use this
    # new field for the report
    financial_statements_report_section = fields.Selection(
        selection=[
            ("assets", "Assets"),
            ("expenses", "Expenses"),
            ("incomes", "Incomes"),
            ("liabilities", "Liabilities"),
        ],
        string="Financial Statements Report - Section",
        compute="_compute_financial_statements_report_section",
        store=True,
        readonly=False,
    )

    @api.depends(
        "account_type",
    )
    def _compute_financial_statements_report_section(self):
        for account in self:
            for section, account_types in SECTION_ACCOUNT_TYPES_DICT.items():
                if account.account_type in account_types:
                    financial_statements_report_section = section
                    break
            else:
                financial_statements_report_section = False
            account.financial_statements_report_section = (
                financial_statements_report_section
            )
