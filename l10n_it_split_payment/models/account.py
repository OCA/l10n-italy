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
from openerp.exceptions import Warning as UserError


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

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        if self.fiscal_position.split_payment:
            self.amount_sp = self.amount_tax
            self.amount_tax = 0
        self.amount_total = self.amount_untaxed + self.amount_tax

    def _build_debit_line(self):
        if not self.company_id.sp_account_id:
            raise UserError(
                _("Please set 'Split Payment Write-off Account' field in"
                  " accounting configuration"))
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
    def _compute_split_payments(self):
        for invoice in self:
            payment_line_ids = invoice.move_line_id_payment_get()
            move_line_pool = self.env['account.move.line']
            for payment_line in move_line_pool.browse(payment_line_ids):
                inv_total = invoice.amount_sp + invoice.amount_total
                payment_line_debit = (
                    invoice.amount_total * payment_line.debit) / inv_total
                payment_line.write(
                    {'debit': payment_line_debit}, update_check=False)

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if (
                invoice.fiscal_position and
                invoice.fiscal_position.split_payment
            ):
                self._compute_split_payments()
                line_model = self.env['account.move.line']
                write_off_line_vals = invoice._build_debit_line()
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.create(write_off_line_vals)
        return res
