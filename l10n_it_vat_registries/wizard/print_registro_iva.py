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
import time

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
        'message': fields.char('Message', size=64, readonly=True),
        }
    _defaults = {
        'type': 'customer',
        'date_from': lambda * a: time.strftime('%Y-%m-%d'),
        'date_to': lambda * a: time.strftime('%Y-%m-%d'),
        #'journal_ids': lambda s, cr, uid, c: s.pool.get('account.journal').search(cr, uid, []),
        }
        
    def counterparts_number(self, move_line):
        counter = 0
        if  not move_line.credit:
            for line in move_line.move_id.line_id:
                if line.credit:
                    counter += 1
        elif not move_line.debit:
            for line in move_line.move_id.line_id:
                if line.debit:
                    counter += 1
        return counter

    def print_registro(self, cr, uid, ids, context=None):
        move_ids = []
        wizard = self.read(cr, uid, ids)[0]
        move_line_obj = self.pool.get('account.move.line')
        tax_pool = self.pool.get('account.tax')
        search_list = []
        search_list = [
            ('journal_id', 'in', wizard['journal_ids']),
            ('move_id.date', '<=', wizard['date_to']),
            ('move_id.date', '>=', wizard['date_from']),
            ('move_id.state', '=', 'posted'),
            ('tax_code_id', '!=', False),
            ]
        move_line_ids = move_line_obj.search(cr, uid, search_list, order='date')
        if context is None:
            context = {}
        for move_line in move_line_obj.browse(cr, uid, move_line_ids):
            # verifico che sia coinvolto un conto imposta legato ad un'imposta tramite conto standard o conto refund
            if move_line.tax_code_id.tax_ids or move_line.tax_code_id.ref_tax_ids:
                if move_line.tax_code_id.tax_ids:
                    if not tax_pool._have_same_rate(move_line.tax_code_id.tax_ids):
                        raise osv.except_osv(_('Error'), _('Taxes %s have different rates')
                            % str(move_line.tax_code_id.tax_ids))
                if move_line.tax_code_id.ref_tax_ids:
                    if not tax_pool._have_same_rate(move_line.tax_code_id.ref_tax_ids):
                        raise osv.except_osv(_('Error'), _('Taxes %s have different rates')
                            % str(move_line.tax_code_id.ref_tax_ids))
                # controllo che ogni tax code abbia una e una sola imposta
                ''' non posso farlo per via dell IVA inclusa nel prezzo
                if len(move_line.tax_code_id.tax_ids) != 1:
                    raise osv.except_osv(_('Error'), _('Wrong tax configuration for tax code %s')
                        % move_line.tax_code_id.name)
                '''
                if move_line.move_id.id not in move_ids:
                    move_ids.append(move_line.move_id.id)
        if not move_ids:
            self.write(cr, uid,  ids, {'message': _('No documents found in the current selection')})
            return True
        datas = {'ids': move_ids}
        datas['model'] = 'account.move'
        datas['form'] = wizard
        datas['move_ids'] = move_ids
        res= {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }
        if wizard['type'] == 'customer':
            res['report_name'] = 'registro_iva_vendite'
        elif wizard['type'] == 'supplier':
            res['report_name'] = 'registro_iva_acquisti'
        elif wizard['type'] == 'corrispettivi':
            res['report_name'] = 'registro_iva_corrispettivi'
        return res

wizard_registro_iva()
