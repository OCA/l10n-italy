# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2012-2015 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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
#

from openerp.osv import fields, orm
from openerp.tools.translate import _


class AccountTaxCode(orm.Model):
    _inherit = 'account.tax.code'
    _columns = {
        'withholding_tax': fields.boolean('Withholding Tax'),
        }


class AccountVoucher(orm.Model):
    _inherit = "account.voucher"

    _columns = {
        'withholding_move_ids': fields.many2many(
            'account.move', 'voucher_withholding_move_rel', 'voucher_id',
            'move_id', 'Withholding Tax Entries', readonly=True),
    }

    def action_move_line_create(self, cr, uid, ids, context=None):
        res = super(AccountVoucher, self).action_move_line_create(
            cr, uid, ids, context)
        inv_pool = self.pool.get('account.invoice')
        curr_pool = self.pool.get('res.currency')
        term_pool = self.pool.get('account.payment.term')
        priod_obj = self.pool.get('account.period')
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        for voucher in self.browse(cr, uid, ids, context):
            amounts_by_invoice = super(
                AccountVoucher, self).allocated_amounts_grouped_by_invoice(
                    cr, uid, voucher, context)
            for inv_id in amounts_by_invoice:
                invoice = inv_pool.browse(cr, uid, inv_id, context)

                move_ids = []
                for tax_line in invoice.tax_line:
                    if (
                        tax_line.tax_code_id and
                        tax_line.tax_code_id.withholding_tax
                    ):
                        # only for supplier payments
                        if voucher.type != 'payment':
                            raise orm.except_orm(
                                _('Error'),
                                _('Can\'t handle withholding tax with voucher '
                                  'of type other than payment'))
                        if not invoice.company_id.withholding_account_id:
                            raise orm.except_orm(
                                _('Error'),
                                _('The company does not have an associated '
                                  'Withholding account'))
                        if not invoice.company_id.withholding_payment_term_id:
                            raise orm.except_orm(
                                _('Error'),
                                _('The company does not have an associated '
                                  'Withholding Payment Term'))
                        if not invoice.company_id.withholding_journal_id:
                            raise orm.except_orm(
                                _('Error'),
                                _('The company does not have an associated '
                                  'Withholding journal'))
                        if not invoice.company_id.authority_partner_id:
                            raise orm.except_orm(
                                _('Error'),
                                _('The company does not have an associated Tax'
                                  ' Authority partner'))

                        # compute the new amount proportionally to paid amount
                        new_line_amount = curr_pool.round(
                            cr, uid, voucher.company_id.currency_id,
                            ((
                                amounts_by_invoice[invoice.id]['allocated'] +
                                amounts_by_invoice[invoice.id]['write-off']
                            ) / invoice.amount_total) * abs(tax_line.amount))

                        # compute the due date
                        due_list = term_pool.compute(
                            cr, uid,
                            invoice.company_id.withholding_payment_term_id.id,
                            new_line_amount,
                            date_ref=voucher.date or invoice.date_invoice,
                            context=context)
                        if len(due_list) > 1:
                            raise orm.except_orm(
                                _('Error'),
                                _('The payment term %s has too many due dates')
                                % invoice.company_id.
                                withholding_payment_term_id.
                                name)
                        if len(due_list) == 0:
                            raise orm.except_orm(
                                _('Error'),
                                _('The payment term %s does not have due '
                                  'dates')
                                % invoice.company_id.
                                withholding_payment_term_id.
                                name)

                        period_ids = priod_obj.find(
                            cr, uid, dt=voucher.date, context=context)
                        new_move = {
                            'journal_id': (
                                invoice.company_id.
                                withholding_journal_id.id),
                            'period_id': period_ids and period_ids[0] or False,
                            'date': voucher.date,
                            'line_id': [
                                (0, 0, {
                                    'name': invoice.number,
                                    'account_id': invoice.account_id.id,
                                    'partner_id': invoice.partner_id.id,
                                    'debit': new_line_amount,
                                    'credit': 0.0,
                                }),
                                (0, 0, {
                                    'name': _(
                                        'Payable withholding - '
                                        ) + invoice.number,
                                    'account_id': (
                                        invoice.company_id.
                                        withholding_account_id.id),
                                    'partner_id': (
                                        invoice.company_id.
                                        authority_partner_id.id),
                                    'debit': 0.0,
                                    'credit': new_line_amount,
                                    'date_maturity': due_list[0][0],
                                }),
                            ]
                        }
                        move_id = move_pool.create(
                            cr, uid, new_move, context=context)
                        move_ids.append(move_id)
                        move = move_pool.browse(
                            cr, uid, move_id, context=context)

                        reconcile_ids = []
                        for invoice_move_line in invoice.move_id.line_id:
                            if (
                                invoice_move_line.account_id.id ==
                                invoice.account_id.id and
                                invoice_move_line.tax_code_id.withholding_tax
                            ):
                                reconcile_ids.append(invoice_move_line.id)
                        for move_line in move.line_id:
                            if (
                                move_line.account_id.id ==
                                invoice.account_id.id
                            ):
                                reconcile_ids.append(move_line.id)
                        move_line_pool.reconcile_partial(
                            cr, uid, reconcile_ids,
                            writeoff_acc_id=voucher.writeoff_acc_id.id,
                            writeoff_period_id=voucher.period_id.id,
                            writeoff_journal_id=voucher.journal_id.id)
                if move_ids:
                    voucher.write(
                        {'withholding_move_ids': [
                            (4, mid) for mid in move_ids]})
        return res

    def cancel_voucher(self, cr, uid, ids, context=None):
        res = super(AccountVoucher, self).cancel_voucher(
            cr, uid, ids, context)
        move_pool = self.pool.get('account.move')
        for voucher in self.browse(cr, uid, ids, context=context):
            for move in voucher.withholding_move_ids:
                move_pool.button_cancel(cr, uid, [move.id])
                move_pool.unlink(cr, uid, [move.id])
        return res
