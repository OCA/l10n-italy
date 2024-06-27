from odoo import models


class OpenItemsReport(models.AbstractModel):
    _inherit = "report.account_financial_report.open_items"

    def _get_net_pay_amounts(self, move_line, original):
        amount_net_pay = original + move_line.withholding_tax_amount
        amount_net_pay_residual = amount_net_pay
        reconciled_amls = move_line.mapped("matched_debit_ids.debit_move_id")
        for line in reconciled_amls:
            if not line.withholding_tax_generated_by_move_id:
                amount_net_pay_residual += line.debit or line.credit
        amount_net_pay_residual = amount_net_pay_residual
        return amount_net_pay, amount_net_pay_residual

    def _get_data(
        self,
        account_ids,
        partner_ids,
        date_at_object,
        only_posted_moves,
        company_id,
        date_from,
    ):
        res = super()._get_data(
            account_ids,
            partner_ids,
            date_at_object,
            only_posted_moves,
            company_id,
            date_from,
        )
        for move_line_vals in res[0]:
            move_line = self.env["account.move.line"].browse(move_line_vals["id"])
            if move_line.move_id.withholding_tax:
                amount_net_pay, amount_net_pay_residual = self._get_net_pay_amounts(
                    move_line, move_line_vals["original"]
                )
                move_line_vals["amount_net_pay"] = amount_net_pay
                move_line_vals["amount_net_pay_residual"] = amount_net_pay_residual
            else:
                move_line_vals["amount_net_pay"] = move_line_vals.get("original")
                move_line_vals["amount_net_pay_residual"] = move_line_vals.get(
                    "amount_residual"
                )
        return res

    def _calculate_amounts(self, open_items_move_lines_data):
        total_amount = super()._calculate_amounts(open_items_move_lines_data)
        for account_id in total_amount:
            total_amount[account_id]["amount_net_pay_residual"] = 0.0
            for partner_id in open_items_move_lines_data[account_id].keys():
                total_amount[account_id][partner_id]["amount_net_pay_residual"] = 0.0
                for move_line_vals in open_items_move_lines_data[account_id][
                    partner_id
                ]:
                    move_line = self.env["account.move.line"].browse(
                        move_line_vals["id"]
                    )
                    _, amount_net_pay_residual = self._get_net_pay_amounts(
                        move_line, move_line_vals["original"]
                    )
                    total_amount[account_id][partner_id][
                        "amount_net_pay_residual"
                    ] += amount_net_pay_residual
                    total_amount[account_id][
                        "amount_net_pay_residual"
                    ] += amount_net_pay_residual
        return total_amount
