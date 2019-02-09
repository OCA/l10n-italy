
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_trunk_line_description = fields.Boolean(
        string='Trunk Line description if exceeds limit of chars'
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fatturapa_trunk_line_description = fields.Boolean(
        related='company_id.fatturapa_trunk_line_description',
        string='Trunk Line description if exceeds limit of chars',
        readonly=False
        )
