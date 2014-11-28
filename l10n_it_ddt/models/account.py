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


from openerp.osv import fields
from openerp.osv import orm


class account_invoice(orm.Model):

    _inherit = 'account.invoice'

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
        'parcels': fields.integer('Number of Packages'),
    }

    def onchange_partner_id(
            self, cr, uid, ids, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False,
            context=None):
        result = super(account_invoice, self).onchange_partner_id(
            cr, uid, ids, type, partner_id, date_invoice, payment_term,
            partner_bank_id, company_id, context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            for k in ('carriage_condition_id',
                      'goods_description_id',
                      'transportation_reason_id',
                      'transportation_method_id'):
                value = getattr(partner, k)
                result['value'][k] = value.id
        return result
