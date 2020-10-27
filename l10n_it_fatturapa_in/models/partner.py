# -*- coding: utf-8 -*-

from openerp import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    e_invoice_default_product_id = fields.Many2one(
        comodel_name='product.product',
        string='E-bill Default Product',
        help="Used by electronic invoice XML import. "
             "If filled, generated invoice lines will use this product, when "
             "no other possible product is found."
    )
    e_invoice_detail_level = fields.Selection([
        ('0', 'Minimum'),
        # ('1', 'Aliquote'),
        ('2', 'Maximum'),
    ], string="E-bills Detail Level",
        help="Minumum level: Bill is created with no lines; "
             "User will have to create them, according to what specified in "
             "the electronic bill.\n"
             # "Livello Aliquote: viene creata una riga fattura per ogni "
             # "aliquota presente nella fattura elettronica\n"
             "Maximum level: every line contained in the electronic bill "
             "will create a line in the bill.",
        default='2', required=True
    )
