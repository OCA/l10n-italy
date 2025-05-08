# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

ACCOUNT_TYPES_NEGATIVE_SIGN = [
    "equity_unaffected",
    "equity",
    "income",
    "income_other",
    "liability_payable",
    "liability_credit_card",
    "asset_prepayments",
    "liability_current",
    "liability_non_current",
]


class Account(models.Model):
    _inherit = "account.account"

    account_balance_sign = fields.Integer(
        string="Balance sign", compute="_compute_account_balance_sign"
    )

    @api.depends("account_type")
    def _compute_account_balance_sign(self):
        for account in self:
            if account.account_type in ACCOUNT_TYPES_NEGATIVE_SIGN:
                account.account_balance_sign = -1
            else:
                account.account_balance_sign = 1
