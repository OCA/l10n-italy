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

from openerp import fields
from openerp import models
from openerp import api
from openerp import netsvc


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

    def action_button_confirm(
        self, cr, uid, ids, context=None
    ):
        res = super(SaleOrder, self).action_button_confirm(
            cr, uid, ids, context=context)
        for order in self.browse(cr, uid, ids, context):
            if order.create_ddt:
                ddt_model = self.pool['stock.ddt']
                ddt_data = {
                    'partner_id': order.partner_id.id,
                    'picking_ids': [(6, 0, [p.id for p in order.picking_ids])],
                    }
                ddt_pool = self.pool['stock.ddt']
                ddt_id = ddt_pool.create(cr, uid, ddt_data, context=context)
                move_lines = []
                for picking in order.picking_ids:
                    move_lines += picking.move_lines
                ddt_pool.create_lines(
                    cr, uid, [ddt_id], move_lines, context=context)
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(
                    uid, 'stock.ddt', ddt_id, 'ddt_confirm', cr)
        return res

    def action_view_ddt(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(
            cr, uid, 'l10n_it_ddt', 'action_stock_ddt')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]

        ddt_ids = []
        for so in self.browse(cr, uid, ids, context=context):
            ddt_ids += [ddt.id for ddt in so.ddt_ids]

        if len(ddt_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(
                map(str, ddt_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(
                cr, uid, 'l10n_it_ddt', 'stock_ddt_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ddt_ids and ddt_ids[0] or False
        return result
