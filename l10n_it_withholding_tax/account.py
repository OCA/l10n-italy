# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012-2013 Associazione OpenERP Italia
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
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
import decimal_precision as dp

class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'withholding_payment_term_id': fields.many2one('account.payment.term', 'Withholding tax Payment Term'),
        'withholding_account_id': fields.many2one('account.account','Withholding account', help='Payable account used for amount due to tax authority', domain=[('type', '=', 'payable')]),
        'withholding_journal_id': fields.many2one('account.journal','Withholding journal', help="Journal used for registration of witholding amounts to be paid"),
        }

class account_invoice(osv.osv):
    
    def _net_pay(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context):
            res[invoice.id] = invoice.amount_total - invoice.withholding_amount
        return res

    _inherit = "account.invoice"

    _columns = {
        'withholding_amount': fields.float('Withholding amount', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft':[('readonly',False)]}),
        'has_withholding': fields.boolean('With withholding tax', readonly=True, states={'draft':[('readonly',False)]}),
        'net_pay': fields.function(_net_pay, string="Net Pay"),
        }

class account_voucher(osv.osv):
    _inherit = "account.voucher"
    
    _columns = {
        'withholding_move_ids': fields.many2many('account.move', 'voucher_withholding_move_rel', 'voucher_id', 'move_id', 'Withholding Tax Entries', readonly=True),
        }
        
    def reconcile_withholding_move(self, cr, uid, invoice, wh_move, context=None):
        line_pool=self.pool.get('account.move.line')
        rec_ids = []
        for inv_move_line in invoice.move_id.line_id:
            if inv_move_line.account_id.type == 'payable' and not inv_move_line.reconcile_id:
                rec_ids.append(inv_move_line.id)
        for wh_line in wh_move.line_id:
            if wh_line.account_id.type == 'payable' and invoice.company_id.withholding_account_id and invoice.company_id.withholding_account_id.id != wh_line.account_id.id and not wh_line.reconcile_id:
                rec_ids.append(wh_line.id)
        return line_pool.reconcile_partial(cr, uid, rec_ids, type='auto', context=context)
    
    def action_move_line_create(self, cr, uid, ids, context=None):
        res = super(account_voucher,self).action_move_line_create(cr, uid, ids, context)
        inv_pool = self.pool.get('account.invoice')
        move_pool = self.pool.get('account.move')
        tax_pool = self.pool.get('account.tax')
        curr_pool = self.pool.get('res.currency')
        term_pool = self.pool.get('account.payment.term')
        for voucher in self.browse(cr, uid, ids, context):
            amounts_by_invoice = super(account_voucher,self).allocated_amounts_grouped_by_invoice(cr, uid,voucher, context)
            for inv_id in amounts_by_invoice:
                invoice = inv_pool.browse(cr, uid, inv_id, context)
                if invoice.withholding_amount:
                    # only for supplier payments
                    if voucher.type != 'payment':
                        raise osv.except_osv(_('Error'), _('Can\'t handle withholding tax with voucher of type other than payment'))
                    if not invoice.company_id.withholding_account_id:
                        raise osv.except_osv(_('Error'), _('The company does not have an associated Withholding account') )
                    if not invoice.company_id.withholding_payment_term_id:
                        raise osv.except_osv(_('Error'), _('The company does not have an associated Withholding Payment Term') )
                    if not invoice.company_id.withholding_journal_id:
                        raise osv.except_osv(_('Error'), _('The company does not have an associated Withholding journal') )
                    # compute the new amount proportionally to paid amount
                    new_line_amount = curr_pool.round(cr, uid, voucher.company_id.currency_id, ((amounts_by_invoice[invoice.id]['allocated'] + amounts_by_invoice[invoice.id]['write-off']) / invoice.net_pay) * invoice.withholding_amount)
                    
                    # compute the due date
                    due_list = term_pool.compute(
                        cr, uid, invoice.company_id.withholding_payment_term_id.id, new_line_amount,
                        date_ref=voucher.date or invoice.date_invoice, context=context)
                    if len(due_list) > 1:
                        raise osv.except_osv(_('Error'),
                            _('The payment term %s has too many due dates')
                            % invoice.company_id.withholding_payment_term_id.name)
                    if len(due_list) == 0:
                        raise osv.except_osv(_('Error'),
                            _('The payment term %s does not have due dates')
                            % invoice.company_id.withholding_payment_term_id.name)
                            
                    new_move = {
                        'journal_id': invoice.company_id.withholding_journal_id.id,
                        'line_id': [
                            (0,0,{
                                'name': invoice.number,
                                'account_id': invoice.account_id.id,
                                'debit': new_line_amount,
                                'credit': 0.0,
                                }),
                            (0,0,{
                                'name': _('Payable withholding - ') + invoice.number,
                                'account_id': invoice.company_id.withholding_account_id.id,
                                'debit': 0.0,
                                'credit': new_line_amount,
                                'date_maturity': due_list[0][0],
                                }),
                            ]
                        }
                    move_id = self.pool.get('account.move').create(cr, uid, new_move, context=context)
                    self.reconcile_withholding_move(cr, uid, invoice, move_pool.browse(cr, uid, move_id, context), context)
                    voucher.write({'withholding_move_ids': [(4, move_id)]})
        return res

    def cancel_voucher(self, cr, uid, ids, context=None):
        res = super(account_voucher,self).cancel_voucher(cr, uid, ids, context)
        reconcile_pool = self.pool.get('account.move.reconcile')
        move_pool = self.pool.get('account.move')
        for voucher in self.browse(cr, uid, ids, context=context):
            recs = []
            for move in voucher.withholding_move_ids:
                move_pool.button_cancel(cr, uid, [move.id])
                move_pool.unlink(cr, uid, [move.id])
        return res
