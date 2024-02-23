# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AssetCategoryDepreciationType(models.Model):
    _name = "asset.category.depreciation.type"
    _description = "Asset Category - Depreciation Type"
    _check_company_auto = True

    base_coeff = fields.Float(
        default=1,
        help="Coeff to compute depreciable amount from purchase amount",
        string="Dep Base Coeff",
    )

    category_id = fields.Many2one(
        "asset.category",
        ondelete="cascade",
        readonly=True,
        required=True,
        string="Category",
        check_company=True,
    )

    company_id = fields.Many2one(
        "res.company", readonly=True, related="category_id.company_id", string="Company"
    )

    depreciation_type_id = fields.Many2one(
        "asset.depreciation.type",
        required=True,
        string="Type",
        check_company=True,
    )

    mode_id = fields.Many2one(
        "asset.depreciation.mode",
        required=True,
        string="Dep Mode",
        check_company=True,
    )

    percentage = fields.Float(string="Depreciation %")

    pro_rata_temporis = fields.Boolean(string="Pro-rata Temporis")

    def get_depreciation_vals(self, amount_depreciable=0):
        self.ensure_one()
        return {
            "amount_depreciable": amount_depreciable * self.base_coeff,
            "base_coeff": self.base_coeff,
            "mode_id": self.mode_id.id,
            "percentage": self.percentage,
            "pro_rata_temporis": self.pro_rata_temporis,
            "type_id": self.depreciation_type_id.id,
        }
