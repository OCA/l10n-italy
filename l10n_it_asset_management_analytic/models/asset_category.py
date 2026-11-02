# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AssetCategory(models.Model):
    _name = "asset.category"
    _inherit = ["asset.category", "analytic.mixin"]
