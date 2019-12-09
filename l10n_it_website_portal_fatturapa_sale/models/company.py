from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    portal_mandatory_e_invoicing = fields.Boolean(
        string='Mandatory e-invoicing for portal customers')
