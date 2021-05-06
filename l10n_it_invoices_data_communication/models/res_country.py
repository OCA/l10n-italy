from odoo import fields, models


class ResCountry(models.Model):
    _inherit = "res.country"

    intrastat = fields.Boolean(string="Intrastat")
