
from odoo import models, fields


class Partner(models.Model):
    _inherit = 'res.partner'

    e_invoice_default_product_id = fields.Many2one(
        comodel_name='product.product',
        string='E-bill Default Product',
        help="Used by electronic invoice XML import. "
             "If filled in, generated bill lines will use this product when "
             "no other possible product is found."
    )
    e_invoice_detail_level = fields.Selection([
        ('0', 'Minimum'),
        ('1', 'Tax Rate'),
        ('2', 'Maximum'),
    ], string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
             "User will have to create them, according to what specified in "
             "the electronic bill.\n"
             "Tax rate level: Rate level: an invoice line is created for each "
             "rate present in the electronic invoice\n"
             "Maximum level: every line contained in the electronic bill "
             "will create a line in the bill.",
        default='2', required=True
    )
