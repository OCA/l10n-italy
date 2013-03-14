# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.osv import orm, fields

class sale_order(orm.Model):
    _inherit = "sale.order"
    _columns =  {
        'validity': fields.date('Validity'),
    }

    def _make_invoice(self, cr, uid, order, lines, context={}):
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context)
        partner = self.pool.get('res.partner').browse(cr , uid, order.partner_id.id)
        self.pool.get('account.invoice').write(cr, uid, inv_id, {
#            'order_id': order.id,
            'carriage_condition_id': partner.carriage_condition_id.id,
            'goods_description_id': partner.goods_description_id.id,
            'transportation_reason_id': partner.transportation_reason_id.id,
            })
        return inv_id

    def action_ship_create(self, cr, uid, ids, *args):
        super(sale_order, self).action_ship_create(cr, uid, ids, *args)
        for order in self.browse(cr, uid, ids, context={}):
            partner = self.pool.get('res.partner').browse(cr , uid, order.partner_id.id)
            picking_obj = self.pool.get('stock.picking')
            picking_ids = picking_obj.search(cr, uid, [('sale_id', '=', order.id)])
            for picking_id in picking_ids:
                picking_obj.write(cr, uid, picking_id, {
#                    'order_id': order.id,
                    'carriage_condition_id': partner.carriage_condition_id.id,
                    'goods_description_id': partner.goods_description_id.id,
                    'transportation_reason_id': partner.transportation_reason_id.id,
                    })
        return True
  
sale_order()


