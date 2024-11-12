from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_74ter_agent = fields.Boolean(string='74ter agent')