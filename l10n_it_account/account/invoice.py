# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2010 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

from openerp.osv import fields, orm
from tools.translate import _

class account_invoice(orm.Model):
    
    _inherit = 'account.invoice'
    _columns = {
        'supplier_invoice_number': fields.char('Supplier invoice nr', size=16),
        }

    def action_number(self, cr, uid, ids, context=None):
        super(account_invoice, self).action_number(cr, uid, ids, context)
        for obj_inv in self.browse(cr, uid, ids):
            inv_type = obj_inv.type

            number = obj_inv.number
            date_invoice = obj_inv.date_invoice
            reg_date = obj_inv.registration_date
            journal = obj_inv.journal_id.id
            inv_type = obj_inv.type
            date_start = obj_inv.registration_date or obj_inv.date_invoice or time.strftime('%Y-%m-%d')
            date_stop = obj_inv.registration_date or obj_inv.date_invoice or time.strftime('%Y-%m-%d')
            period_ids = self.pool.get('account.period').search(
                cr, uid, [('date_start','<=',date_start),('date_stop','>=',date_stop), 
                ('company_id', '=', obj_inv.company_id.id)])
            if inv_type == 'out_invoice' or inv_type == 'out_refund':
                #check if another invoice with a minor number and a superior date_invoice is posted
                res = self.search(cr, uid, [('type','=',inv_type),('date_invoice','>',date_invoice), 
                    ('number', '<', number), ('journal_id','=',journal),('period_id','in',period_ids)])
                if res:
                    raise orm.except_orm(_('Date Inconsistency'),
                            _('Cannot create invoice! xxxx Post the invoice with a greater date'))
            if inv_type == 'in_invoice' or inv_type == 'in_refund':
                #check if an invoice with a superior registration_date is posted
                res = self.search(cr, uid, [('type','=',inv_type),('registration_date','>',reg_date), 
                    ('journal_id','=',journal),('period_id','in',period_ids)], context=context)
                if res:
                    raise orm.except_orm(_('Date Inconsistency'),
                        _('Cannot create invoice! Post the invoice with a greater date'))
                #check duplication (only supplier's invoices)
                supplier_invoice_number = obj_inv.supplier_invoice_number
                partner_id = obj_inv.partner_id.id
                res = self.search(cr, uid, [('type','=',inv_type),('date_invoice','=',date_invoice), 
                    ('journal_id','=',journal),('supplier_invoice_number','=',supplier_invoice_number),
                    ('partner_id','=',partner_id),('state','not in',('draft','cancel'))], context=context)
                if res:
                    raise orm.except_orm(_('Invoice Duplication'),
                        _('Invoice already posted!'))
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
