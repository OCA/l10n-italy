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

import netsvc
import pooler, tools

from openerp.osv import orm, fields
from tools.translate import _

class account_invoice(orm.Model):
    
    _inherit = 'account.invoice'
        
    _columns = {
#        'order_id':fields.many2one('sale.order','Sale Order'),
        'carriage_condition_id': fields.many2one('stock.picking.carriage_condition', 'Carriage condition'),
        'goods_description_id': fields.many2one('stock.picking.goods_description', 'Description of goods'),
        'transportation_reason_id': fields.many2one('stock.picking.transportation_reason', 'Reason for transportation'),
        }

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        result = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,
            date_invoice, payment_term, partner_bank_id, company_id)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            result['value']['carriage_condition_id'] = partner.carriage_condition_id.id
            result['value']['goods_description_id'] = partner.goods_description_id.id
            result['value']['transportation_reason_id'] = partner.transportation_reason_id.id
        return result
    
account_invoice()

