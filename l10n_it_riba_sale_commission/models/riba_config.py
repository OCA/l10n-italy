from odoo import models, fields


class RibaConfiguration(models.Model):

    _inherit = "riba.configuration"

    safety_days = fields.Integer("Safety days", default=5)
