# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AssetDepreciationType(models.Model):
    _name = "asset.depreciation.type"
    _description = "Asset Depreciation Type"
    _order = "name"

    @api.model
    def get_default_company_id(self):
        return self.env.company

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, string="Company"
    )

    name = fields.Char(required=True)

    print_by_default = fields.Boolean(
        default=True,
        help="Defines whether a category should be added by default when"
        " printing assets' reports.",
    )

    requires_account_move = fields.Boolean()

    @api.ondelete(
        at_uninstall=False,
    )
    def _unlink_except_in_category(self):
        if (
            self.env["asset.category.depreciation.type"]
            .sudo()
            .search([("depreciation_type_id", "in", self.ids)])
        ):
            raise UserError(
                _(
                    "Cannot delete depreciation types while they're still used"
                    " by categories."
                )
            )
