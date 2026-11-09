from odoo import api, models


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    @api.model
    def _compute_account_amount(
        self, total_amount, tb_initial_acc, tb_period_acc, foreign_currency
    ):
        total_amount = super()._compute_account_amount(
            total_amount, tb_initial_acc, tb_period_acc, foreign_currency
        )
        for tb in tb_initial_acc:
            acc_id = tb["account_id"]
            if tb["account_internal_group"] in ["expense", "income"]:
                total_amount[acc_id]["initial_balance"] = 0.0
                total_amount[acc_id]["ending_balance"] = total_amount[acc_id]["balance"]
                if foreign_currency:
                    total_amount[acc_id]["initial_currency_balance"] = 0.0
                    total_amount[acc_id]["ending_currency_balance"] += round(
                        total_amount[acc_id]["amount_currency"], 2
                    )
        return total_amount
