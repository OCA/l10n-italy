# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    def _get_report_values(self, docids, data):
        if data.get("ignore_closing_move"):
            self = self.with_context(trial_balance_ignore_closing_move=True)
        return super()._get_report_values(docids, data)

    def _add_ignore_closing_move_domain(self, domain):
        if self.env.context.get("trial_balance_ignore_closing_move"):
            # Moves not created by the fiscal year closing procedure
            domain += [("move_id.closing_type", "in", ["none", False])]
        return domain

    def _get_initial_balances_bs_ml_domain(self, *args, **kwargs):
        return self._add_ignore_closing_move_domain(
            super()._get_initial_balances_bs_ml_domain(*args, **kwargs)
        )

    def _get_initial_balances_pl_ml_domain(self, *args, **kwargs):
        return self._add_ignore_closing_move_domain(
            super()._get_initial_balances_pl_ml_domain(*args, **kwargs)
        )

    def _get_period_ml_domain(self, *args, **kwargs):
        return self._add_ignore_closing_move_domain(
            super()._get_period_ml_domain(*args, **kwargs)
        )

    def _get_initial_balance_fy_pl_ml_domain(self, *args, **kwargs):
        return self._add_ignore_closing_move_domain(
            super()._get_initial_balance_fy_pl_ml_domain(*args, **kwargs)
        )
