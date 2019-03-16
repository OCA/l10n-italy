
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_cut_off_line_description = fields.Boolean(
        string='Cut off line description if exceeds limit of chars'
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fatturapa_cut_off_line_description = fields.Boolean(
        related='company_id.fatturapa_trunk_line_description',
        string='Cut off line description if exceeds limit of chars',
        readonly=False
        )
