# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#    Copyright 2018 Andrea Cometa - Apulia Software
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

from osv import orm, fields,osv
from tools.translate import _
import decimal_precision as dp


class AccountFiscalPosition(osv.osv):
    _inherit = 'account.fiscal.position'

    _columns = {
        'split_payment': fields.boolean("Split Payment")
    }


class AccountInvoice(osv.osv):
    _inherit = 'account.invoice'

    def _amount_all(self, cr, uid, ids, name, args, context=None):
        res = super(AccountInvoice, self)._amount_all(
            cr, uid, ids, name, args, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id]['amount_sp'] = 0
            if invoice.split_payment:
                res[invoice.id]['amount_sp'] = res[invoice.id]['amount_tax']
                res[invoice.id]['amount_tax'] = 0
            res[invoice.id]['amount_total'] = res[invoice.id][
                'amount_untaxed'] + res[invoice.id]['amount_tax']
        print res
        return res

    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(
                cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(
                cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()

    _columns = {
        'amount_untaxed': fields.function(
            _amount_all, digits_compute=dp.get_precision('Account'),
            string='Untaxed', multi='all',
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['invoice_line', 'fiscal_position'], 20),
                'account.invoice.tax': (
                    _get_invoice_tax, None, 20),
                'account.invoice.line': (
                    _get_invoice_line, ['price_unit', 'invoice_line_tax_id',
                                        'quantity', 'discount', 'invoice_id'],
                    20),
            }),
        'amount_tax': fields.function(
            _amount_all, digits_compute=dp.get_precision('Account'),
            string='Untaxed', multi='all',
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['invoice_line', 'fiscal_position'], 20),
                'account.invoice.tax': (
                    _get_invoice_tax, None, 20),
                'account.invoice.line': (
                    _get_invoice_line, ['price_unit', 'invoice_line_tax_id',
                                        'quantity', 'discount', 'invoice_id'],
                    20),
            }),
        'amount_total': fields.function(
            _amount_all, digits_compute=dp.get_precision('Account'),
            string='Untaxed', multi='all',
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['invoice_line', 'fiscal_position'], 20),
                'account.invoice.tax': (
                    _get_invoice_tax, None, 20),
                'account.invoice.line': (
                    _get_invoice_line, ['price_unit', 'invoice_line_tax_id',
                                        'quantity', 'discount', 'invoice_id'],
                    20),
            }),
        'amount_sp': fields.function(
            _amount_all, digits_compute=dp.get_precision('Account'),
            string='Untaxed', multi='all',
            store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids,
                    ['invoice_line', 'fiscal_position'], 20),
                'account.invoice.tax': (
                    _get_invoice_tax, None, 20),
                'account.invoice.line': (
                    _get_invoice_line, ['price_unit', 'invoice_line_tax_id',
                                        'quantity', 'discount', 'invoice_id'],
                    20),
            }),
        'split_payment': fields.related(
            'fiscal_position', 'split_payment',
            string="Split Payment", type='boolean')
    }

    def _build_debit_line(self, cr, uid, ids, context=None):
        invoices = self.browse(cr, uid, ids, context=context)
        for invoice in invoices:
            if not invoice.company_id.sp_account_id:
                raise orm.except_orm(
                    _("Warning!"),
                    _("Please set 'Split Payment Write-off Account' field in"
                      " accounting configuration"))
            vals = {
                'name': _('Split Payment Write Off'),
                'partner_id': invoice.partner_id.id,
                'account_id': invoice.company_id.sp_account_id.id,
                'journal_id': invoice.journal_id.id,
                'period_id': invoice.period_id.id,
                'date': invoice.date_invoice,
                'debit': invoice.amount_sp,
                'credit': 0,
                }
            if invoice.type == 'out_refund':
                vals['debit'] = 0
                vals['credit'] = invoice.amount_sp
        return vals

    def _compute_split_payments(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context=context):
            payment_line_ids = invoice.move_line_id_payment_get()
            move_line_pool = self.pool['account.move.line']
            for payment_line in move_line_pool.browse(
                    cr, uid, payment_line_ids, context=context):
                inv_total = invoice.amount_sp + invoice.amount_total
                if invoice.type == 'out_invoice':
                    payment_line_amount = (
                        invoice.amount_total * payment_line.debit) / inv_total
                    payment_line.write(
                        {'debit': payment_line_amount},
                        context=context, update_check=False)
                elif invoice.type == 'out_refund':
                    payment_line_amount = (
                        invoice.amount_total * payment_line.credit) / inv_total
                    payment_line.write(
                        {'credit': payment_line_amount},
                        context=context, update_check=False)

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(AccountInvoice, self).action_move_create(
            cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            if (
                invoice.fiscal_position and
                invoice.fiscal_position.split_payment
            ):
                if invoice.type in ['in_invoice', 'in_refund']:
                    raise orm.except_orm(
                        _("Warning!"),
                        _("Can't handle supplier invoices with split payment"))
                invoice._compute_split_payments()
                line_model = self.pool['account.move.line']
                write_off_line_vals = invoice._build_debit_line()
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.create(cr, uid, write_off_line_vals, context=context)
        return res
