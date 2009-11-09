# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 Domsense SRL (<http://www.domsense.com>).
#    All Rights Reserved
#    $Id$
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

import netsvc
import pooler, tools

from osv import fields, osv

class stock_picking_carriage_condition(osv.osv):
    """
    Carriage condition
    """
    _name = "stock.picking.carriage_condition"
    _description = "Carriage Condition"
    _columns = {
	'name':fields.char('Carriage Condition', size=64, required=True, readonly=False),
	'note': fields.text('Note'),
    }
stock_picking_carriage_condition()

class stock_picking_goods_description(osv.osv):
    """
    Description of Goods
    """
    _name = 'stock.picking.goods_description'
    _description = "Description of Goods"

    _columns = {
	'name':fields.char('Description of Goods', size=64, required=True, readonly=False),
	'note': fields.text('Note'),
    }
stock_picking_goods_description()


class stock_picking_reason(osv.osv):
    """
    Reason for Transportation
    """
    _name = 'stock.picking.transportation_reason'
    _description = 'Reason for transportation'

    _columns = {
	'name':fields.char('Reason For Transportation', size=64, required=True, readonly=False),
	'note': fields.text('Note'),
    }
stock_picking_reason()

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns =  {
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'address_id': fields.many2one('res.partner', 'Location Address'),
        'carriage_condition_id': fields.many2one('stock.picking.carriage_condition', 'Carriage condition'),
        'goods_description_id': fields.many2one('stock.picking.goods_description', 'Description of goods'),
        'transportation_reason_id': fields.many2one('stock.picking.transportation_reason', 'Reason for transportation'),
        'lines_amount': fields.integer('Lines amount'),
    }
    _defaults = {
        'company_id': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid,context=context).company_id.id,
    }

    def _items_amount(self, cr, uid, ids, name, args, context=None):
        res = {}
        for pack in self.browse(cr,uid,ids, context=context):
            amount=0
            for move_line in pack.move_lines:
                amount=amount+int(move_line.product_qty)
        return amount

    def button_compute(self, cr, uid, ids, context=None):
        for pack in self.browse(cr,uid,ids):
            amount=0
            for move_line in pack.move_lines:
                amount=amount+int(move_line.product_qty)
        self.pool.get('stock.picking').write(cr, uid, [pack.id], {'lines_amount': amount})
        return True

    def draft_validate(self, cr, uid, ids, *args):
        self.button_compute(cr, uid, ids)
        wf_service = netsvc.LocalService("workflow")
        self.draft_force_assign(cr, uid, ids)
        for pick in self.browse(cr, uid, ids):
            move_ids = [x.id for x in pick.move_lines]
            self.pool.get('stock.move').force_assign(cr, uid, move_ids)
            wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
            self.action_move(cr, uid, [pick.id])
            wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_done', cr)
        return True

    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='/'):
	    if 'type' in vals.keys() and vals['type']=='out':
            	vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'stock.picking_out')
	    elif 'type' in vals.keys() and vals['type']=='internal':
            	vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'stock.picking_internal')
	    else:
		vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'stock.picking_in')		

        return super(stock_picking, self).create(cr, user, vals, context)


stock_picking()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:



