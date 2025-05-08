#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AssetComputeDepreciableAmount(models.AbstractModel):
    _name = "l10n_it_asset_management.compute.depreciable_amount"
    _description = "Compute depreciable amount"

    base_coeff = fields.Float(
        default=1,
        help="Coeff to compute depreciable amount from purchase amount",
        string="Dep Base Coeff",
    )
    base_max_amount = fields.Float(
        string="Maximum depreciable amount",
    )

    def _get_depreciable_amount(self, base_amount):
        """Compute how much of `base_amount` can be depreciated."""
        self.ensure_one()
        depreciable_amount = base_amount
        if self.base_coeff:
            depreciable_amount = base_amount * self.base_coeff
        if self.base_max_amount:
            depreciable_amount = min(depreciable_amount, self.base_max_amount)
        return depreciable_amount
