# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AssetDepreciation(models.Model):
    _inherit = "asset.depreciation"

    def get_dismiss_account_move_line_vals(self):
        vals_list = super().get_dismiss_account_move_line_vals()
        return self.env["asset.depreciation.line"]._set_move_lines_analytic(
            vals_list, self.l10n_it_asset_id.analytic_distribution
        )
