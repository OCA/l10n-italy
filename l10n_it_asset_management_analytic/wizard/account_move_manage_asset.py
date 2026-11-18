# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class WizardAccountMoveManageAsset(models.TransientModel):
    _inherit = "wizard.account.move.manage.asset"

    def get_create_asset_vals(self):
        vals = super().get_create_asset_vals()
        # Use the distribution of the move lines when they all have the same
        distributions = {
            frozenset((line.analytic_distribution or {}).items())
            for line in self.move_line_ids
        }
        if len(distributions) == 1:
            distribution = self.move_line_ids[:1].analytic_distribution
            if distribution:
                vals["analytic_distribution"] = distribution
        return vals
