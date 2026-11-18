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
