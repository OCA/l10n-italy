# -*- encoding: utf-8 -*-
from openerp import models
from openerp import fields


class ateco_category(models.Model):
    _name = 'ateco.category'
    _description = 'ATECO Code'

    name = fields.Char(
        'Name',
        size=180,
        required=True
    )
    code = fields.Char(
        'ATECO Code',
        size=10,
        required=False
    )
    description = fields.Text(
        'Description'
    )
    parent_id = fields.Many2one(
        'ateco.category',
        'Parent Category',
        select=True
    )
    child_ids = fields.One2many(
        'ateco.category',
        'parent_id',
        'Child Categories'
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'ateco_category_partner_rel',
        'ateco_id',
        'partner_id',
        'Partners'
    )
