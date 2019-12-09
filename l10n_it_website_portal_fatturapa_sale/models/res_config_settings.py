from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    portal_mandatory_e_invoicing = fields.Boolean(
        related='company_id.portal_mandatory_e_invoicing',
        string="Mandatory e-invoicing for portal customers", readonly=False)
