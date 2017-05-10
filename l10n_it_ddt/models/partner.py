# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', string='Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Method of Transportation')
    ddt_invoicing_group = fields.Selection(
        [('nothing', 'One DDT - One Invoice'),
         ('billing_partner', 'Billing Partner'),
         ('shipping_partner', 'Shipping Partner'),
         ('code_group', 'Code group')], 'DDT invoicing group',
        default='billing_partner')
    ddt_code_group = fields.Char(string='Code group')
    ddt_show_price = fields.Boolean(
        string='DDT show prices', default=False, help="Show prices and \
        discounts in ddt report")
