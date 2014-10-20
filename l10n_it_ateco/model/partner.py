# -*- encoding: utf-8 -*-
from openerp import models
from openerp import fields


class res_partner(models.Model):
    _inherit = 'res.partner'

    ateco_category_ids = fields.Many2many(
        'ateco.category',
        'ateco_category_partner_rel',
        'partner_id',
        'ateco_id',
        'Ateco categories'
    )
