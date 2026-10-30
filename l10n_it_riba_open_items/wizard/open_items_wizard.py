# Copyright 2026 nextev.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OpenItemsReportWizard(models.TransientModel):
    _inherit = "open.items.report.wizard"

    show_riba_uncovered = fields.Boolean(
        string="Show RiBa uncovered",
        default=True,
        help="Include invoices closed by a RiBa acceptance whose RiBa has not "
        "yet been paid, with zero balance and the uncovered amount in a "
        "dedicated column.",
    )

    def _prepare_report_open_items(self):
        res = super()._prepare_report_open_items()
        res["show_riba_uncovered"] = self.show_riba_uncovered
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
