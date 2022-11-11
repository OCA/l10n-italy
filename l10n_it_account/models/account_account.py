# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

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
        default=1,
        string="Balance sign",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "account_balance_sign" not in vals and "account_type" in vals:
                if vals["account_type"] in ACCOUNT_TYPES_NEGATIVE_SIGN:
                    vals["account_balance_sign"] = -1
        return super().create(vals_list)

    @api.model
    def set_account_types_negative_sign(self):
        for account_type in ACCOUNT_TYPES_NEGATIVE_SIGN:
            account_ids = self.env["account.account"].search(
                [("account_type", "=", account_type)]
            )
            for account_id in account_ids:
                account_id.with_context(
                    skip_check_balance_sign_coherence=True
                ).account_balance_sign = -1

    def check_balance_sign_value(self):
        """
        Checks whether `account_balance_sign` gets a correct value of +1 or -1.
        """
        if any(t.account_balance_sign not in (-1, 1) for t in self):
            raise ValidationError(_("Balance sign's value can only be 1 or -1."))

    @api.constrains("account_balance_sign")
    def check_balance_sign_coherence(self):
        """
        Checks whether changes upon `account_balance_sign` create incoherencies
        in account groups' balance signs.
        """
        self.check_balance_sign_value()

        acc_obj = self.env["account.account"]
        key_val_dict = dict(self._fields["account_type"].selection)
        for key in key_val_dict:
            accounts = acc_obj.search(
                [("account_type", "=", key)],
            )
            # Avoid check upon empty recordset to make it faster
            if accounts:
                accounts.check_balance_sign_coherence_group()

    @api.constrains("group_id")
    def check_balance_sign_coherence_group(self):
        """
        Checks whether adding an account to (or removing it from) a group
        creates incoherencies in account groups' balance signs.
        """
        groups = self.mapped("group_id")
        # Avoid check upon empty recordset to make it faster
        if groups:
            groups.check_balance_sign_coherence()

    def have_same_sign(self):
        """
        Checks account' signs.
        :return: True if there's nothing to check or there's only one account
        to check; else, returns True or False according to whether every
        account has the same value for `account_balance_sign` (if it's not 0).
        """
        to_check = self.filtered(lambda a: a.account_balance_sign)
        if len(to_check) <= 1:
            return True
        benchmark = to_check[0].account_balance_sign
        return all(a.account_balance_sign == benchmark for a in to_check)
