

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = "res.country"

    intrastat = fields.Boolean(
        string='Intrastat')
