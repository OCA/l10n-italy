# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

ACCOUNT_TYPES_NEGATIVE_SIGN = [
    "account.data_unaffected_earnings",
    "account.data_account_type_equity",
    "account.data_account_type_revenue",
    "account.data_account_type_other_income",
    "account.data_account_type_payable",
    "account.data_account_type_credit_card",
    "account.data_account_type_prepayments",
    "account.data_account_type_current_liabilities",
    "account.data_account_type_non_current_liabilities",
]


class AccountType(models.Model):
    _inherit = "account.account.type"

    account_balance_sign = fields.Integer(
        default=1,
        string="Balance sign",
    )

    @api.model
    def set_account_types_negative_sign(self):
        for xml_id in ACCOUNT_TYPES_NEGATIVE_SIGN:
            acc_type = self.env.ref(xml_id, raise_if_not_found=False)
            if acc_type:
                acc_type.with_context(
                    skip_check_balance_sign_coherence=True
                ).account_balance_sign = -1

    @api.constrains("account_balance_sign")
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
        # Force check upon sign itself before checking groups signs coherence
        self.check_balance_sign_value()
        acc_obj = self.env["account.account"]
        for account_type in self:
            accounts = acc_obj.search([("user_type_id", "=", account_type.id)])
            # Avoid check upon empty recordset to make it faster
            if accounts:
                accounts.check_balance_sign_coherence()

    def have_same_sign(self):
        """
        Checks types' signs.
        :return: True if there's nothing to check or there's only one type
        to check; else, returns True or False according to whether every
        type has the same value for `account_balance_sign` (if it's not 0).
        """
        to_check = self.filtered(lambda t: t.account_balance_sign)
        if len(to_check) <= 1:
            return True
        benchmark = to_check[0].account_balance_sign
        return all(t.account_balance_sign == benchmark for t in to_check)
