# © 2020 Andrei Levin <andrei.levin@didotech.com>

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoices_group_by_partner = fields.Boolean('Multi Invoice XML', help="Permit to pack more invoices in one XML")


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoices_group_by_partner = fields.Boolean(
        related='company_id.invoices_group_by_partner',
        string='Multi Invoice XML',
        help="Permit to pack more invoices in single XML",
        readonly=False
    )
