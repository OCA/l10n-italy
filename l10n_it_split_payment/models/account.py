# -*- coding: utf-8 -*-
# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.addons.decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError


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
        related='fiscal_position_id.split_payment')


    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount')
    def _compute_amount(self):
        for invoice in self:
            super(AccountInvoice, invoice)._compute_amount()
            invoice.amount_sp = 0
            if invoice.fiscal_position_id.split_payment:
                invoice.amount_sp = invoice.amount_tax
                invoice.amount_tax = 0
            invoice.amount_total = invoice.amount_untaxed + invoice.amount_tax

    def _build_debit_line(self):
        if not self.company_id.sp_account_id:
            raise UserError(
                _("Please set 'Split Payment Write-off Account' field in"
                  " accounting configuration"))
        vals = {
            'name': _('Split Payment Write Off'),
            'partner_id': self.partner_id.id,
            'account_id': self.company_id.sp_account_id.id,
            'journal_id': self.journal_id.id,
            'period_id': self.period_id.id,
            'date': self.date_invoice,
            'debit': self.amount_sp,
            'credit': 0,
            }
        if self.type == 'out_refund':
            vals['debit'] = 0
            vals['credit'] = self.amount_sp
        return vals

    @api.multi
    def _compute_split_payments(self):
        for invoice in self:
            payment_line_ids = invoice.move_line_id_payment_get()
            move_line_pool = self.env['account.move.line']
            for payment_line in move_line_pool.browse(payment_line_ids):
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


    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if (
                invoice.fiscal_position_id and
                invoice.fiscal_position_id.split_payment
            ):
                if invoice.type in ['in_invoice', 'in_refund']:
                    raise UserError(
                        _("Can't handle supplier invoices with split payment"))
                self._compute_split_payments()
                line_model = self.env['account.move.line']
                write_off_line_vals = invoice._build_debit_line()
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.create(write_off_line_vals)
        return res
