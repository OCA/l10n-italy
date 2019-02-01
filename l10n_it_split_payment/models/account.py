# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
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

import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

from openerp.osv import fields, orm


class AccountFiscalPosition(orm.Model):
    _inherit = 'account.fiscal.position'
    _columns = {
        'split_payment': fields.boolean('Split Payment'),
        }


class AccountInvoice(orm.Model):

    def _compute_amounts(self, cr, uid, ids, field_name, arg, context=None):
        amount_res = self.pool['account.invoice']._amount_all(
            cr, uid, ids, field_name, arg, context)
        for invoice in self.browse(cr, uid, ids, context):
            amount_res[invoice.id]['amount_sp'] = 0
            if invoice.fiscal_position.split_payment:
                amount_res[invoice.id]['amount_sp'] = amount_res[
                    invoice.id]['amount_tax']
                amount_res[invoice.id]['amount_tax'] = 0
                amount_res[invoice.id]['amount_total'] = amount_res[
                    invoice.id]['amount_untaxed'] + amount_res[
                        invoice.id]['amount_tax']
        return amount_res

    def _get_invoice_by_tax(self, cr, uid, ids, context=None):
        return self.pool['account.invoice']._get_invoice_tax(
            cr, uid, ids, context=context)

    def _get_invoice_by_line(self, cr, uid, ids, context=None):
        return self.pool['account.invoice']._get_invoice_line(
            cr, uid, ids, context=context)

    _inherit = 'account.invoice'
    _columns = {
        'amount_sp': fields.function(
            _compute_amounts, string='Split Payment',
            digits_compute=dp.get_precision('Account'),
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, [
                    'invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_by_tax, None, 20),
                'account.invoice.line': (_get_invoice_by_line, [
                    'price_unit', 'invoice_line_tax_id', 'quantity',
                    'discount', 'invoice_id'], 20),
                },
            multi='all'
            ),
        'amount_untaxed': fields.function(
            _compute_amounts, digits_compute=dp.get_precision('Account'),
            string='Subtotal', track_visibility='always',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, [
                    'invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_by_tax, None, 20),
                'account.invoice.line': (_get_invoice_by_line, [
                    'price_unit', 'invoice_line_tax_id', 'quantity',
                    'discount', 'invoice_id'], 20),
            },
            multi='all'),
        'amount_tax': fields.function(
            _compute_amounts, digits_compute=dp.get_precision('Account'),
            string='Tax',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, [
                    'invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_by_tax, None, 20),
                'account.invoice.line': (_get_invoice_by_line, [
                    'price_unit', 'invoice_line_tax_id', 'quantity',
                    'discount', 'invoice_id'], 20),
            },
            multi='all'),
        'amount_total': fields.function(
            _compute_amounts, digits_compute=dp.get_precision('Account'),
            string='Total',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, [
                    'invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_by_tax, None, 20),
                'account.invoice.line': (_get_invoice_by_line, [
                    'price_unit', 'invoice_line_tax_id', 'quantity',
                    'discount', 'invoice_id'], 20),
            },
            multi='all'),
        'split_payment': fields.related(
            'fiscal_position', 'split_payment', type='boolean',
            string='Split Payment'),
        }

    def _build_debit_line(self, invoice):
        if not invoice.company_id.sp_account_id:
            raise orm.except_orm(
                _('Error'),
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
        for invoice in self.browse(cr, uid, ids, context):
            payment_line_ids = invoice.move_line_id_payment_get(cr, uid, ids)
            move_line_pool = self.pool['account.move.line']
            for payment_line in move_line_pool.browse(
                cr, uid, payment_line_ids, context
            ):
                inv_total = invoice.amount_sp + invoice.amount_total
                if invoice.type == 'out_invoice':
                    payment_line_amount = (
                        invoice.amount_total * payment_line.debit) / inv_total
                    payment_line.write(
                        {'debit': payment_line_amount}, update_check=False)
                elif invoice.type == 'out_refund':
                    payment_line_amount = (
                        invoice.amount_total * payment_line.credit) / inv_total
                    payment_line.write(
                        {'credit': payment_line_amount}, update_check=False)

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(AccountInvoice, self).action_move_create(
            cr, uid, ids, context=context)
        for invoice in self.browse(cr, uid, ids, context):
            if (
                invoice.fiscal_position and
                invoice.fiscal_position.split_payment
            ):
                if invoice.type in ['in_invoice', 'in_refund']:
                    raise orm.except_orm(
                        _('Error'),
                        _("Can't handle supplier invoices with split payment"))
                invoice._compute_split_payments()
                line_model = self.pool['account.move.line']
                write_off_line_vals = self._build_debit_line(invoice)
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.create(
                    cr, uid, write_off_line_vals, context=context)
                # trigger recompute of amount_residual
                self.write(cr, uid, ids, {'invoice_line': []}, context=context)
        return res
