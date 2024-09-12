from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    govway_url = fields.Char(
        string="GovWay URL",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    govway_url = fields.Char(
        string="GovWay URL",
        related="company_id.govway_url",
        readonly=True,
    )
