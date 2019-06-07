from odoo import models, fields, api

ACCOUNT_TYPES_NEGATIVE_SIGN = [
    'account.data_unaffected_earnings',
    'account.data_account_type_revenue',
    'account.data_account_type_other_income',
    'account.data_account_type_payable',
    'account.data_account_type_credit_card',
    'account.data_account_type_prepayments',
    'account.data_account_type_current_liabilities',
    'account.data_account_type_non_current_liabilities',
]


class AccountType(models.Model):
    _inherit = 'account.account.type'
    account_balance_sign = fields.Integer("Balance sign", default=1)

    @api.model
    def set_account_types_negative_sign(self):
        for xml_id in ACCOUNT_TYPES_NEGATIVE_SIGN:
            acc_type = self.env.ref(xml_id, raise_if_not_found=False)
            if acc_type:
                acc_type.account_balance_sign = -1
