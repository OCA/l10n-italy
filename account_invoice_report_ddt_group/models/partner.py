# -*- coding: utf-8 -*-


from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    ddt_invoice_print_shipping_address = fields.Boolean(
        string='DDT invoice print shipping address', default=False,
        help="Show shipping address of DDT in the invoice report")
