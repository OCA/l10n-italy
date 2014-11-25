# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.one
    def _get_ddt_ids(self):
        picking_model = self.env['stock.picking']
        pickings = picking_model.search([('origin', '=', self.name)])
        self.ddt_ids = [picking.ddt_id.id for picking in pickings]

    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', 'Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description', 'Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        'Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        'Method of Transportation')
    parcels = fields.Integer()
    ddt_ids = fields.Many2many(
        'stock.ddt',
        string='Related DdTs',
        compute='_get_ddt_ids',
        )
    create_ddt = fields.Boolean('Automatically create the DDT', default=True)

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        if not context:
            context = {}
        result = super(SaleOrder, self).onchange_partner_id(
            cr, uid, ids, partner_id, context=context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            result['value'][
                'carriage_condition_id'] = partner.carriage_condition_id.id
            result['value'][
                'goods_description_id'] = partner.goods_description_id.id
            result['value'][
                'transportation_reason_id'
                ] = partner.transportation_reason_id.id
            result['value'][
                'transportation_method_id'
                ] = partner.transportation_method_id.id
        return result

    def _make_invoice(self, cr, uid, order, lines, context={}):
        inv_id = super(SaleOrder, self)._make_invoice(
            cr, uid, order, lines, context)
        partner = self.pool.get('res.partner').browse(
            cr, uid, order.partner_id.id)
        self.pool.get('account.invoice').write(cr, uid, inv_id, {
            'carriage_condition_id': partner.carriage_condition_id.id,
            'goods_description_id': partner.goods_description_id.id,
            'transportation_reason_id': partner.transportation_reason_id.id,
            'transportation_method_id': partner.transportation_method_id.id,
            })
        return inv_id

    def action_ship_create(self, cr, uid, ids, *args):
        super(SaleOrder, self).action_ship_create(cr, uid, ids, *args)
        for order in self.browse(cr, uid, ids, context={}):
            partner = self.pool.get('res.partner').browse(
                cr, uid, order.partner_id.id)
            picking_obj = self.pool.get('stock.picking')
            picking_ids = picking_obj.search(
                cr, uid, [('sale_id', '=', order.id)])
            for picking_id in picking_ids:
                picking_obj.write(cr, uid, picking_id, {
                    'carriage_condition_id': partner.carriage_condition_id.id,
                    'goods_description_id': partner.goods_description_id.id,
                    'transportation_reason_id':
                    partner.transportation_reason_id.id,
                    'transportation_method_id':
                    partner.transportation_method_id.id,
                    'parcels': order.parcels,
                    })
        return True

    def _prepare_procurement_group(self, cr, uid, order, context=None):
        res = super(SaleOrder, self)._prepare_procurement_group(
            cr, uid, order, context=context)
        if order.create_ddt:
            ddt_model = self.pool['stock.ddt']
            ddt_data = {
                'partner_id': order.partner_id.id,
                'partner_shipping_id': order.partner_shipping_id and
                order.partner_shipping_id.id
                }
            res['ddt_id'] = ddt_model.create(
                cr, uid, ddt_data, context=context)
        return res
