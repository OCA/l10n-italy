# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Asset(models.Model):
    _name = "asset.asset"
    _inherit = ["asset.asset", "analytic.mixin"]

    @api.depends("category_id")
    def _compute_analytic_distribution(self):
        for asset in self:
            if not asset.analytic_distribution:
                asset.analytic_distribution = asset.category_id.analytic_distribution
