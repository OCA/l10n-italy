# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AssetDepreciationLine(models.Model):
    _name = "asset.depreciation.line"
    _inherit = ["asset.depreciation.line", "analytic.mixin"]

    @api.depends("depreciation_id")
    def _compute_analytic_distribution(self):
        # The line keeps the distribution the asset had when it was created
        for line in self:
            if not line.analytic_distribution:
                line.analytic_distribution = line.l10n_it_asset_id.analytic_distribution

    @api.model
    def _set_move_lines_analytic(self, vals_list, distribution):
        """Set `distribution` on the income and expense lines of `vals_list`.

        The other lines (asset, depreciation fund) are not changed:
        they follow the analytic distribution models as usual.
        Without `distribution`, `vals_list` is not changed.
        """
        if not distribution:
            return vals_list
        account_model = self.env["account.account"]
        for vals in vals_list:
            account = account_model.browse(vals.get("account_id"))
            if account.internal_group in ("income", "expense"):
                vals["analytic_distribution"] = distribution
        return vals_list

    def get_depreciated_account_move_line_vals(self):
        vals_list = super().get_depreciated_account_move_line_vals()
        return self._set_move_lines_analytic(vals_list, self.analytic_distribution)

    def get_gain_account_move_line_vals(self):
        vals_list = super().get_gain_account_move_line_vals()
        return self._set_move_lines_analytic(vals_list, self.analytic_distribution)

    def get_loss_account_move_line_vals(self):
        vals_list = super().get_loss_account_move_line_vals()
        return self._set_move_lines_analytic(vals_list, self.analytic_distribution)
