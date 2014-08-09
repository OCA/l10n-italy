# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Davide Corio <davide.corio@lsweb.it>
#    Copyright (C) 2014 L.S. Advanced Software srl
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

from openerp.osv import orm, fields


class stock_picking_carriage_condition(orm.Model):
    _name = "stock.picking.carriage_condition"
    _description = "Carriage Condition"
    _columns = {
        'name': fields.char(
            'Carriage Condition', size=64, required=True),
        'note': fields.text('Note'),
    }


class stock_picking_goods_description(orm.Model):
    _name = 'stock.picking.goods_description'
    _description = "Description of Goods"

    _columns = {
        'name': fields.char(
            'Description of Goods', size=64, required=True),
        'note': fields.text('Note'),
    }


class stock_picking_transportation_reason(orm.Model):
    _name = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    _columns = {
        'name': fields.char(
            'Reason For Transportation', size=64, required=True),
        'note': fields.text('Note'),
    }


class stock_picking_transportation_method(orm.Model):
    _name = 'stock.picking.transportation_method'
    _description = 'Method of Transportation'

    _columns = {
        'name': fields.char(
            'Method of Transportation', size=64, required=True),
        'note': fields.text('Note'),
    }


class stock_picking(orm.Model):
    _inherit = "stock.picking"
    _columns = {
        'carriage_condition_id': fields.many2one(
            'stock.picking.carriage_condition', 'Carriage Condition'),
        'goods_description_id': fields.many2one(
            'stock.picking.goods_description', 'Description of Goods'),
        'transportation_reason_id': fields.many2one(
            'stock.picking.transportation_reason',
            'Reason for Transportation'),
        'transportation_method_id': fields.many2one(
            'stock.picking.transportation_method',
            'Method of Transportation'),
        'ddt_number':  fields.char('DDT', size=64),
        'ddt_date':  fields.date('DDT date'),
        'ddt_type': fields.related('picking_type_id', 'code', type='char',
            string='DDT Type'),
    }

    def action_invoice_create(
            self, cr, uid, ids, journal_id, group=False, type='out_invoice',
            context=None):
        if not context:
            context = {}
        invoice_obj = self.pool['account.invoice']
        res = super(stock_picking, self).action_invoice_create(
            cr, uid, ids, journal_id, group, type, context)
        for picking in self.browse(cr, uid, ids, context=context):
            invoice_obj.write(cr, uid, res, {
                'carriage_condition_id':
                picking.carriage_condition_id and
                picking.carriage_condition_id.id,
                'goods_description_id':
                picking.goods_description_id and
                picking.goods_description_id.id,
                'transportation_reason_id':
                picking.transportation_reason_id and
                picking.transportation_reason_id.id,
                'transportation_method_id':
                picking.transportation_method_id and
                picking.transportation_method_id.id,
                })
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        if not context:
            context = {}
        default.update({'ddt_number': ''})
        return super(stock_picking, self).copy(
            cr, uid, id, default, context=context)
