# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import fields, models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.one
    def _get_ddt_ids(self):
        ddt_ids = []
        for picking in self.picking_ids:
            for ddt in picking.ddt_ids:
                ddt_ids.append(ddt.id)
        self.ddt_ids = ddt_ids

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
        'stock.picking.package.preparation',
        string='Related DdTs',
        compute='_get_ddt_ids', )
    create_ddt = fields.Boolean('Automatically create the DDT')

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

    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_id = super(SaleOrder, self)._make_invoice(
            cr, uid, order, lines, context)
        self.pool.get('account.invoice').write(cr, uid, [inv_id], {
            'carriage_condition_id': order.carriage_condition_id.id,
            'goods_description_id': order.goods_description_id.id,
            'transportation_reason_id': order.transportation_reason_id.id,
            'transportation_method_id': order.transportation_method_id.id,
            })
        return inv_id

    def action_ship_create(self, cr, uid, ids, context=None):
        res = super(SaleOrder, self).action_ship_create(
            cr, uid, ids, context=context)
        ddt_pool = self.pool['stock.picking.package.preparation']
        for order in self.browse(cr, uid, ids, context):
            if order.create_ddt:
                picking_ids = [p.id for p in order.picking_ids]
                ddt_data = {
                    'partner_id': order.partner_id.id,
                    'partner_invoice_id': order.partner_id.id,
                    'partner_shipping_id': order.partner_id.id,
                    'carriage_condition_id': order.carriage_condition_id.id,
                    'goods_description_id': order.goods_description_id.id,
                    'transportation_reason_id':
                    order.transportation_reason_id.id,
                    'transportation_method_id':
                    order.transportation_method_id.id,
                    'picking_ids': [(6, 0, picking_ids)],
                    }
                ddt_pool.create(cr, uid, ddt_data, context)
        return res

    def action_view_ddt(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(
            cr, uid, 'stock_picking_package_preparation',
            'action_stock_picking_package_preparation')
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
                cr, uid, 'stock_picking_package_preparation',
                'stock_picking_package_preparation_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ddt_ids and ddt_ids[0] or False
        return result
