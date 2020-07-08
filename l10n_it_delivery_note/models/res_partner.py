# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    default_transport_condition_id = fields.Many2one(
        'stock.picking.transport.condition',
        string=_("Condition of transport"))
    default_goods_appearance_id = fields.Many2one(
        'stock.picking.goods.appearance', string=_("Appearance of goods"))
    default_transport_reason_id = fields.Many2one(
        'stock.picking.transport.reason', string=_("Reason of transport"))
    default_transport_method_id = fields.Many2one(
        'stock.picking.transport.method', string=_("Method of transport"))
