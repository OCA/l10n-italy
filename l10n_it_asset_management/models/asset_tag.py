# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AssetTag(models.Model):
    _name = "asset.tag"
    _description = "Asset Tags"

    @api.model
    def get_default_company_id(self):
        return self.env.company

    company_id = fields.Many2one(
        "res.company", default=get_default_company_id, string="Company"
    )

    name = fields.Char(required=True)
