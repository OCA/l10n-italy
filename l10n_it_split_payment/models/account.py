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
from openerp import models, fields, api, _


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    split_payment = fields.Boolean('Split Payment')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    amount_sp = fields.Float(
        string='Split Payment',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount')
    split_payment = fields.Boolean(
        'Split Payment',
        related='fiscal_position.split_payment')
    sp_move_id = fields.Many2one(
        'account.move',
        string='Split Payment Write-off')

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        if self.fiscal_position.split_payment:
            self.amount_sp = self.amount_tax
            self.amount_tax = 0
        self.amount_total = self.amount_untaxed + self.amount_tax

    def reconcile_sp(self, sp_line):
        reconcile_set = sp_line
        for line in self.move_id.line_id:
            if line.account_id.id == sp_line.account_id.id:
                reconcile_set += line
        reconcile_set.reconcile_partial()

    def _build_credit_vals(self):
        return {
            'name': _('Split Payment Write Off'),
            'partner_id': self.partner_id.id,
            'account_id': self.account_id.id,
            'journal_id': self.journal_id.id,
            'period_id': self.period_id.id,
            'date': self.date_invoice,
            'credit': self.amount_sp,
            'debit': 0,
            }

    def _build_debit_line(self):
        return {
            'name': _('Split Payment Write Off'),
            'partner_id': self.partner_id.id,
            'account_id': self.company_id.sp_account_id.id,
            'journal_id': self.journal_id.id,
            'period_id': self.period_id.id,
            'date': self.date_invoice,
            'debit': self.amount_sp,
            'credit': 0,
            }

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if (
                invoice.fiscal_position and
                invoice.fiscal_position.split_payment
            ):
                line_model = self.env['account.move.line']
                credit_line_vals = invoice._build_credit_vals()
                write_off_line_vals = invoice._build_debit_line()
                sp_journal_id = invoice.company_id.sp_journal_id
                move_model = self.env['account.move']
                move_data = {
                    'journal_id': sp_journal_id.id,
                    'date': invoice.date_invoice,
                    'period_id': invoice.period_id.id,
                }
                move = move_model.create(move_data)
                credit_line_vals['move_id'] = move.id
                write_off_line_vals['move_id'] = move.id
                invoice.sp_move_id = move.id
                credit_line = line_model.create(credit_line_vals)
                line_model.create(write_off_line_vals)
                move.post()
                invoice.reconcile_sp(credit_line)
        return res

    def _is_unreconciliable(self):
        inv_credit_lines = 0
        for line in self.move_id.line_id:
            if line.account_id.type == 'receivable':
                inv_credit_lines += 1
        for line in self.sp_move_id.line_id:
            if line.account_id.type == 'receivable':
                if line.reconcile_partial_id:
                    if len(
                        line.reconcile_partial_id.line_partial_ids
                    ) == inv_credit_lines + 1:
                        # if reconciliation only contains invoice credit
                        # + split payment
                        return True
        return False

    def _unreconcile_sp(self):
        for line in self.sp_move_id.line_id:
            if line.account_id.type == 'receivable':
                line.reconcile_partial_id.unlink()

    @api.multi
    def action_cancel(self):
        for inv in self:
            if inv._is_unreconciliable():
                inv._unreconcile_sp()
        res = super(AccountInvoice, self).action_cancel()
        moves = self.env['account.move']
        for inv in self:
            moves += inv.sp_move_id
        if moves:
            moves.button_cancel()
            moves.unlink()
        return res
