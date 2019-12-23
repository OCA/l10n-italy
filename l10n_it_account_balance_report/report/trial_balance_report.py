# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.tools import float_is_zero


class TrialBalanceReportAccount(models.TransientModel):
    _inherit = 'report_trial_balance_account'

    def _compute_hide_line(self):
        """
        Method _compute_hide_line hides lines which have debit, credit,
        initial_balance and final_balance all set to 0 (or small enough to
        simply ignore them), but when we try to create an Account Balance
        report, the only data we need is the final_balance field.
        Therefore, we set as hidden every line created for our report which
        has final_balance = 0 (in case the user chooses to hide accounts at 0).
        """
        super()._compute_hide_line()

        balance_line_obj = self.env['account_balance_report_account']
        balance_line_domain = [('trial_balance_line_id', 'in', self.ids)]
        balance_lines = balance_line_obj.search(balance_line_domain)
        lines_to_recompute = balance_lines.mapped('trial_balance_line_id')

        # If we use the Trial Balance wizard, no balance line will be
        # created and assigned to a trial line; therefore, lines_to_recompute
        # will be an empty recordset.
        # Viceversa, if we use the Account Balance wizard, every balance
        # line created will be linked to a trial line; therefore,
        # lines_to_recompute will be self itself.
        for line in lines_to_recompute:
            trial_report = line.report_id
            balance = line.final_balance
            currency = line.currency_id or trial_report.company_id.currency_id
            rounding = currency.rounding
            if trial_report.hide_account_at_0 \
                    and float_is_zero(balance, precision_rounding=rounding):
                line.hide_line = True

    def get_balance_sign(self):
        sign = 1
        if self.account_id:
            sign = self.account_id.user_type_id.account_balance_sign
        elif self.account_group_id:
            sign = self.account_group_id.account_balance_sign
        return sign
