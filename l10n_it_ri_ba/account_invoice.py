# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    All Rights Reserved 
#    Thanks to Cecchi s.r.l http://www.cecchi.com/
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

from datetime import datetime

from osv import fields, osv
from tools.translate import _

class Invoice(osv.osv):
    _inherit = 'account.invoice'

    def search_move_id_riba(self, cr, uid, ids, context):
       """Invoices on Payments_Term Riba True"""
       cr.execute(""" SELECT ai.move_id
          FROM account_invoice ai
          INNER JOIN account_payment_term pt ON (ai.payment_term = pt.id)
          WHERE pt.riba = 'True'""")
       return [x[0] for x in cr.fetchall()]


    def action_process_riba(self, cr, uid, ids, context=None):
        if not ids: return []
        inv = self.browse(cr, uid, ids[0], context=context)
        if inv.payment_term.riba is True:
          return {
            'name':_("Pay Invoice"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {
                'default_partner_id': inv.partner_id.id,
                'default_amount': inv.residual,
                'default_name':inv.internal_number,
                'close_after_process': True,
                'invoice_type':inv.type,
                'invoice_id':inv.id,
                'default_type': inv.type in ('out_invoice') and 'receipt' or 'payment'
                }
        }
 
Invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
