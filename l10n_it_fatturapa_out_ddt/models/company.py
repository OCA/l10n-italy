
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_ddt_shipping_address = fields.Boolean(
        string='Shipping address in XML',
        default=True
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fatturapa_ddt_shipping_address = fields.Boolean(
        related='company_id.fatturapa_ddt_shipping_address',
        string='Shipping address in XML',
        readonly=False
        )
