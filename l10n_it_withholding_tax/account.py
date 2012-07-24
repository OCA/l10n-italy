# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _

# TODO creare la tax ritenuta
class account_tax(osv.osv):
    _inherit = 'account.tax'
    _columns = {
        'withholding_tax': fields.boolean('Withholding Tax'),
        'withholding_payment_term_id': fields.many2one('account.payment.term', 'Withholding Payment Term'),
        'withholding_account_id': fields.many2one('account.account','Withholding account', help='Payable account used for amount due to tax authority'),
        'withholding_journal_id': fields.many2one('account.journal','Withholding journal'),
        }

class account_voucher(osv.osv):
    _inherit = "account.voucher"
    
    _columns = {
        'withholding_move_id': fields.many2one('account.move','Withholding Entry', readonly=True),
        }
    
    def is_withholding_move_line(self, cr , uid, line_id, context=None):
        move_line = self.pool.get('account.move.line').browse(cr, uid, line_id, context)
        tax_pool = self.pool.get('account.tax')
        tax_ids = tax_pool.search(cr, uid, [('tax_code_id', '=', move_line.tax_code_id.id)])
        is_withholding = False
        for tax in tax_pool.browse(cr, uid, tax_ids):
            if tax.withholding_tax:
                is_withholding = True
        return is_withholding
        
    def get_withholding_tax(self, cr, uid, move_line_id, context=None):
        move_line = self.pool.get('account.move.line').browse(cr, uid, move_line_id, context)
        tax_ids = tax_pool.search(cr, uid, [('tax_code_id', '=', move_line.tax_code_id.id)])
        if len(tax_ids) > 1:
            raise osv.except_osv(_('Error'),
                _('Too many taxes associated to tax.code %s') % move_line.tax_code_id.name)
        if not tax_ids:
            raise osv.except_osv(_('Error'),
                _('No taxes associated to tax.code %s') % move_line.tax_code_id.name)
        return tax_ids[0]
    
    def action_move_line_create(self, cr, uid, ids, context=None):
        res = super(account_voucher,self).action_move_line_create(cr, uid, ids, context)
        inv_pool = self.pool.get('account.invoice')
        tax_pool = self.pool.get('account.tax')
        for voucher in self.browse(cr, uid, ids, context):
            amounts_by_invoice = super(account_voucher,self).allocated_amounts_grouped_by_invoice(cr, uid,voucher, context)
            for inv_id in amounts_by_invoice:
                invoice = inv_pool.browse(cr, uid, inv_id, context)
                for move_line in invoice.move_id.line_id:
                    if self.is_withholding_move_line(cr , uid, move_line.id, context):
                        if voucher.type != 'payment':
                            raise osv.except_osv(_('Error'), _('Can\'t handle withholding tax with voucher of type other than payment'))
                        wh_tax = tax_pool.browse(cr, uid, self.get_withholding_tax(cr, uid, move_line.id, context), context)
                        if not wh_tax.withholding_account_id:
                            raise osv.except_osv(_('Error'), _('The tax %s does not have an associated Withholding account') % wh_tax.name)
                        if not wh_tax.withholding_payment_term_id:
                            raise osv.except_osv(_('Error'), _('The tax %s does not have an associated Withholding Payment Term') % wh_tax.name)
                        if not wh_tax.withholding_journal_id:
                            raise osv.except_osv(_('Error'), _('The tax %s does not have an associated Withholding journal') % wh_tax.name)
                        # compute the new amount proportionally to paid amount
                        new_line_amount = currency_obj.round(cr, uid, voucher.company_id.currency_id, ((amounts_by_invoice[invoice.id]['allocated'] + amounts_by_invoice[invoice.id]['write-off']) / amounts_by_invoice[invoice.id]['total']) * (move_line.credit or move_line.debit))
                        new_move = {
                            'journal_id': wh_tax.withholding_journal_id.id,
                            'line_id': [
                                (0,0,{
                                    'name'
                                    }),
                                ]
                            }
        return res

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    
    def action_move_create(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).action_move_create(cr, uid, ids, context=context)
        tax_pool = self.pool.get('account.tax')
        term_pool = self.pool.get('account.payment.term')
        for inv in self.browse(cr, uid, ids, context=context):
            for move_line in inv.move_id.line_id:
                if move_line.tax_code_id:
                    
                        if tax.withholding_tax and tax.withholding_payment_term_id:
                            due_list = term_pool.compute(
                                cr, uid, tax.withholding_payment_term_id.id, move_line.tax_amount,
                                date_ref=inv.date_invoice, context=context)
                            if len(due_list) > 1:
                                raise osv.except_osv(_('Error'),
                                    _('The payment term %s has too many due dates')
                                    % tax.withholding_payment_term_id.name)
                            if len(due_list) == 0:
                                raise osv.except_osv(_('Error'),
                                    _('The payment term %s does not have due dates')
                                    % tax.withholding_payment_term_id.name)
                            move_line.write({'date_maturity': due_list[0][0]})
        return res

