from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_74ter_agent = fields.Boolean(string='74ter agency')
    agent_74ter_id = fields.Many2one("res.partner", string="Agency")
    invoices_paid_by_agent = fields.Boolean()