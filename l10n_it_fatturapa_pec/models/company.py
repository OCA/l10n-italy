# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    e_invoice_user_id = fields.Many2one(
        "res.users", "E-bill creator",
        help="This user will be used at supplier e-bill creation.",
        default=lambda self: self.env.user.id
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    e_invoice_user_id = fields.Many2one(
        related='company_id.e_invoice_user_id',
        readonly=False,
    )
