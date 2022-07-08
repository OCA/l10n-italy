# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.tools import float_is_zero


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    def _remove_accounts_at_cero(self, total_amount, show_partner_details, company):
        """Full override of method to compute accounts to hide

        Method that remove account which have debit, credit,
        initial_balance and ending_balance all set to 0 (or small enough to
        simply ignore them), but when we try to create an Account Balance
        Report, the only data we need is the ending_balance field.
        """
        def is_removable(d):
            rounding = company.currency_id.rounding
            return float_is_zero(d["ending_balance"], precision_rounding=rounding)

        accounts_to_remove = []
        for acc_id, ta_data in total_amount.items():
            if is_removable(ta_data):
                accounts_to_remove.append(acc_id)
            elif show_partner_details:
                partner_to_remove = []
                for key, value in ta_data.items():
                    # If the show_partner_details option is checked,
                    # the partner data is in the same account data dict
                    # but with the partner id as the key
                    if isinstance(key, int) and is_removable(value):
                        partner_to_remove.append(key)
                for partner_id in partner_to_remove:
                    del ta_data[partner_id]
        for account_id in accounts_to_remove:
            del total_amount[account_id]
