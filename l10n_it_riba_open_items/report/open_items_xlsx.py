# Copyright 2026 nextev.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models


class OpenItemsXslx(models.AbstractModel):
    _inherit = "report.a_f_r.report_open_items_xlsx"

    def _get_report_columns(self, report):
        res = super()._get_report_columns(report)
        if report.show_riba_uncovered:
            res[max(res) + 1] = {
                "header": _("RiBa uncovered"),
                "field": "riba_uncovered",
                "field_final_balance": "riba_uncovered",
                "type": "amount",
                "width": 14,
            }
        return res

    def _get_report_filters(self, report):
        res = super()._get_report_filters(report)
        res.append(
            [
                _("Show RiBa uncovered"),
                _("Yes") if report.show_riba_uncovered else _("No"),
            ]
        )
        return res

    def _calculate_amounts_by_partner(self, account_id, open_items_move_lines_data):
        total_amount = super()._calculate_amounts_by_partner(
            account_id, open_items_move_lines_data
        )
        for line in open_items_move_lines_data:
            totals = total_amount[account_id][line["partner_id"]]
            totals.setdefault("riba_uncovered", 0.0)
            totals["riba_uncovered"] += line.get("riba_uncovered", 0.0)
        return total_amount

    def write_ending_balance_from_dict(
        self,
        my_object,
        type_object,
        total_amount,
        report_data,
        account_id=False,
        partner_id=False,
    ):
        if type_object in ("partner", "partner_subtotal"):
            totals = total_amount[account_id][partner_id]
        else:
            totals = total_amount[account_id]
        my_object["riba_uncovered"] = totals.get("riba_uncovered", 0.0)
        return super().write_ending_balance_from_dict(
            my_object,
            type_object,
            total_amount,
            report_data,
            account_id=account_id,
            partner_id=partner_id,
        )
