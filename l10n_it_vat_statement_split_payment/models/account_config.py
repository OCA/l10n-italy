# Copyright 2018 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sp_description = fields.Char(
        related="company_id.sp_description",
        string="Description for period end statements",
        readonly=False,
    )
