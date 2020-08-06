# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from .sale import TD_INVOICING_GROUPS


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
        TD_INVOICING_GROUPS, 'TD invoicing group',
        default='billing_partner',
        required=True,
    )
    ddt_code_group = fields.Char(string='Code group')
    ddt_show_price = fields.Boolean(
        string='TD show prices', help='Show prices and discounts in TD report')
    ddt_invoice_exclude = fields.Boolean(
        string='Do not invoice services from DDT',
        help="If flagged services will not be automatically "
             "invoiced from DDT. If set on the partner, this parameter will"
             "be automatically applied to Sale Orders.")
