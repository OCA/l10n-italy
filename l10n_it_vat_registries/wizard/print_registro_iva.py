# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
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

from osv import fields,osv
from tools.translate import _

class wizard_registro_iva(osv.osv_memory):

    _name = "wizard.registro.iva"
    _columns = {
        'date_from': fields.date('From date', required=True),
        'date_to': fields.date('To date', required=True),
        'type': fields.selection([
            ('customer', 'Customer Invoices'),
            ('supplier', 'Supplier Invoices'),
            ('corrispettivi', 'Corrispettivi'),
            ], 'Type', required=True),
        'journal_ids': fields.many2many('account.journal', 'registro_iva_journals_rel', 'journal_id', 'registro_id', 'Journals', help='Select journals you want retrieve documents from', required=True),
    }

    def print_registro(self, cr, uid, ids, context=None):
        inv_ids = []
        wizard = self.read(cr, uid, ids)[0]
        inv_obj = self.pool.get('account.invoice')
        search_list = []
        if wizard['type'] == 'customer':
            search_list = [
                ('journal_id', 'in', wizard.journal_ids),
                ('corrispettivo', '=', False),
                ('move_id.date', '<=', wizard['date_to']),
                ('move_id.date', '>=', wizard['date_from']),
                '|',
                ('type', '=', 'out_invoice'),
                ('type', '=', 'out_refund'),
                '|',
                ('state', '=', 'open'),
                ('state', '=', 'paid'),
                ]
        elif wizard['type'] == 'supplier':
            search_list = [
                ('journal_id', 'in', wizard.journal_ids),
                ('corrispettivo', '=', False),
                ('move_id.date', '<=', wizard['date_to']),
                ('move_id.date', '>=', wizard['date_from']),
                '|',
                ('type', '=', 'in_invoice'),
                ('type', '=', 'in_refund'),
                '|',
                ('state', '=', 'open'),
                ('state', '=', 'paid'),
                ]
        elif wizard['type'] == 'corrispettivi':
            search_list = [
                ('journal_id', 'in', wizard.journal_ids),
                ('corrispettivo', '=', True),
                ('move_id.date', '<=', wizard['date_to']),
                ('move_id.date', '>=', wizard['date_from']),
                '|',
                ('type', '=', 'out_invoice'),
                ('type', '=', 'out_refund'),
                '|',
                ('state', '=', 'open'),
                ('state', '=', 'paid'),
                ]
        inv_ids = inv_obj.search(cr, uid, search_list)
        if not inv_ids:
            raise osv.except_osv(_('Error !'), _('No documents found in the selected date range'))
        if context is None:
            context = {}
        datas = {'ids': inv_ids}
        datas['model'] = 'account.invoice'
        datas['form'] = wizard
        datas['inv_ids'] = inv_ids
        res= {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }
        if wizard['type'] == 'customer' or wizard['type'] == 'corrispettivi':
            res['report_name'] = 'registro_iva_vendite'
        elif wizard['type'] == 'supplier':
            res['report_name'] = 'registro_iva_acquisti'
        return res

wizard_registro_iva()
