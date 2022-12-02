# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AssetDepreciationMode(models.Model):
    _name = "asset.depreciation.mode"
    _description = "Asset Depreciation Mode"
    _order = "name"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, string="Company"
    )

    default = fields.Boolean(string="Default Mode")

    line_ids = fields.One2many(
        "asset.depreciation.mode.line", "mode_id", string="Lines"
    )

    name = fields.Char(
        required=True,
        string="Name",
    )

    used_asset_coeff = fields.Float(
        default=1.0,
        string="Used Asset Coeff.",
    )

    def copy(self, default=None):
        default = dict(default or [])
        default.update(
            {
                "default": False,
                "line_ids": [
                    (0, 0, line.copy_data({"mode_id": False})[0])
                    for line in self.line_ids
                ],
            }
        )
        return super().copy(default)

    def unlink(self):
        if (
            self.env["asset.category.depreciation.type"]
            .sudo()
            .search([("mode_id", "in", self.ids)])
        ):
            raise UserError(
                _(
                    "Cannot delete depreciation modes while they're still linked"
                    " to categories."
                )
            )
        if self.env["asset.depreciation"].sudo().search([("mode_id", "in", self.ids)]):
            raise UserError(
                _(
                    "Cannot delete depreciation modes while they're still linked"
                    " to depreciations."
                )
            )
        return super().unlink()

    @api.constrains("company_id", "default")
    def check_default_modes(self):
        for company in self.mapped("company_id"):
            domain = [("company_id", "=", company.id), ("default", "=", True)]
            if self.search_count(domain) > 1:
                raise ValidationError(
                    _(
                        "There can be no more than 1 default depreciation mode"
                        " for each company."
                    )
                )

    def get_depreciation_amount_multiplier(self):
        multiplier = 1
        if not self:
            return multiplier

        self.ensure_one()

        # Update multiplier from used asset coefficient
        used_asset = self._context.get("used_asset", False)
        if self.used_asset_coeff and used_asset:
            multiplier *= self.used_asset_coeff

        # Update multiplier from lines
        lines = self.line_ids
        if lines:
            multiplier *= lines.get_depreciation_amount_multiplier()

        return multiplier
