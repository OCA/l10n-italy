# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 OpenERP Italian Community (<http://www.openerp-italia.org>).
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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree
from tools.translate import _
from osv import osv, fields

class riba_order_create(osv.osv_memory):
    """
    Create a riba object with lines corresponding to the account move line
    to pay according to the date and the mode provided by the user.
    Hypothesis:
    - Small number of non-reconcilied move line, riba mode and bank account type,
    - Big number of partner and bank account.

    If a type is given, unsuitable account Entry lines are ignored.
    """

    _name = 'riba.order.create'
    _description = 'riba.order.create'
    _columns = {
        'duedate': fields.date('Due Date', required=True),
        'entries': fields.many2many('account.move.line', 'line_pay_rel', 'pay_id', 'line_id', 'Entries')
    }
    _defaults = {
         'duedate': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(riba_order_create, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=False)
        if context and 'line_ids' in context:
            view_obj = etree.XML(res['arch'])
            child = view_obj.getchildren()[0]
            domain = '[("id", "in", '+ str(context['line_ids'])+')]'
            field = etree.Element('field', attrib={'domain': domain, 'name':'entries', 'colspan':'4', 'height':'300', 'width':'800', 'nolabel':"1"})
            child.addprevious(field)
            res['arch'] = etree.tostring(view_obj)
        return res

    def create_riba(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('riba.order')
        line_obj = self.pool.get('account.move.line')
        riba_obj = self.pool.get('riba.line')
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        line_ids = [entry.id for entry in data.entries]
        if not line_ids:
            return {'type': 'ir.actions.act_window_close'}

        riba = order_obj.browse(cr, uid, context['active_id'], context=context)
        t = None
        line2bank = line_obj.line2bank(cr, uid, line_ids, t, context)
        line2iban = line_obj.line2iban(cr, uid, line_ids, t, context)
        
        ## Finally populate the current riba with new lines:
        for line in line_obj.browse(cr, uid, line_ids, context=context):
            if riba.date_prefered == "now":
                #no riba date => immediate payment
                date_to_pay = False
            elif riba.date_prefered == 'due':
                date_to_pay = line.date_maturity
            elif riba.date_prefered == 'fixed':
                date_to_pay = riba.date_scheduled
            iban = []
            if line2iban.get(line.id):
                iban = line2iban.get(line.id)
            else:
                raise osv.except_osv('Error', _('For one o more partner(s) NO has been specified IBAN '))        
            riba_obj.create(cr, uid,{
                'move_line_id': line.id,
                'amount_currency': line.amount_to_pay,
                'bank_id': line2bank.get(line.id),
                'order_id': riba.id,
                'partner_id': line.partner_id and line.partner_id.id or False,
                'communication': line.ref or '/',
                'date': date_to_pay,
                'currency': line.invoice and line.invoice.currency_id.id or False,
                }, context=context)
        return {'type': 'ir.actions.act_window_close'}

    def search_entries(self, cr, uid, ids, context=None):
        line_obj = self.pool.get('account.move.line')
        mod_obj = self.pool.get('ir.model.data')
        invoice_obj = self.pool.get('account.invoice')
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        move_id = invoice_obj.search_move_id_riba(cr, uid, ids, context)       
        search_due_date = data.duedate
        # Search for move line to pay:
        domain = [('account_id.type', '=', 'receivable'), ('amount_to_pay', '>', 0), ('move_id', 'in', move_id)]
        domain = domain + ['|', ('date_maturity', '<=', search_due_date), ('date_maturity', '=', False)]
        line_ids = line_obj.search(cr, uid, domain, context=context)
        context.update({'line_ids': line_ids})
        model_data_ids = mod_obj.search(cr, uid,[('model', '=', 'ir.ui.view'), ('name', '=', 'view_riba_order_create_lines')], context=context)
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)[0]['res_id']
        return {'name': ('Entrie Lines'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'riba.order.create',
                'views': [(resource_id,'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
        }

riba_order_create()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
