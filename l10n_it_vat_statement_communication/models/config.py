# -*- coding: utf-8 -*-


from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    vsc_supply_code = fields.Char(
        'Vat statement communication supply code',
        help="ES: IVP18")

