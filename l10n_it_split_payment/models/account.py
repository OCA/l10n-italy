# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
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


class AccountInvoiceTax(models.Model):
    _inherit = 'account.invoice.tax'

    @api.v8
    def compute(self, invoice):
        res = super(AccountInvoiceTax, self).compute(invoice)
        fp = invoice.fiscal_position
        if fp and fp.split_payment:
            for group in res:
                account_id = res[group]['account_id']
                for map in fp.account_ids:
                    if map.account_src_id.id == account_id:
                        res[group]['account_id'] = map.account_dest_id.id
                        new_group = (group[0], group[1], map.account_dest_id.id)
                        res[new_group] = res[group]
                        res.pop(group)
        return res


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
    sp_type = fields.Selection(
        string='Split Payment Type', related='company_id.sp_type')
    sp_move_id = fields.Many2one(
        'account.move',
        string='Split Payment Write-off')

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = sum(
            line.price_subtotal for line in self.invoice_line)
        if self.fiscal_position.split_payment:
            self.amount_sp = sum(line.amount for line in self.tax_line)
            self.amount_tax = 0
        else:
            self.amount_tax = sum(line.amount for line in self.tax_line)
            self.amount_sp = 0
        self.amount_total = self.amount_untaxed + self.amount_tax

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        if self.fiscal_position and self.fiscal_position.split_payment:
            line_model = self.env['account.move.line']
            sp_type = self.company_id.sp_type
            sp_account_id = self.company_id.sp_account_id
            if sp_type == '1-entry':
                credit_line = {
                    'name': _('Split Payment Write Off'),
                    'move_id': self.move_id.id,
                    'partner_id': self.partner_id.id,
                    'account_id': self.account_id.id,
                    'journal_id': self.journal_id.id,
                    'period_id': self.period_id.id,
                    'date': self.date_invoice,
                    'credit': self.amount_sp,
                    'debit': 0}
                line_model.create(credit_line)
                write_off_line = {
                    'name': _('Split Payment Write Off'),
                    'move_id': self.move_id.id,
                    'partner_id': self.partner_id.id,
                    'account_id': sp_account_id.id,
                    'journal_id': self.journal_id.id,
                    'period_id': self.period_id.id,
                    'date': self.date_invoice,
                    'debit': self.amount_sp,
                    'credit': 0}
                line_model.create(write_off_line)
            else:
                sp_journal_id = self.company_id.sp_journal_id
                move_model = self.env['account.move']
                move_data = {
                    'journal_id': sp_journal_id.id,
                    'date': self.date_invoice,
                    'period_id': self.period_id.id,
                }
                move = move_model.create(move_data)
                credit_line = {
                    'name': _('Split Payment Write Off'),
                    'move_id': move.id,
                    'partner_id': self.partner_id.id,
                    'account_id': self.account_id.id,
                    'journal_id': move.journal_id.id,
                    'period_id': move.period_id.id,
                    'date': move.date,
                    'credit': self.amount_sp,
                    'debit': 0}
                line_model.create(credit_line)
                write_off_line = {
                    'name': _('Split Payment Write Off'),
                    'move_id': move.id,
                    'partner_id': self.partner_id.id,
                    'account_id': sp_account_id.id,
                    'journal_id': move.journal_id.id,
                    'period_id': move.period_id.id,
                    'date': move.date,
                    'debit': self.amount_sp,
                    'credit': 0}
                line_model.create(write_off_line)
                self.sp_move_id = move.id
        return res
