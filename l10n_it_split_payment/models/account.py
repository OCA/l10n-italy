# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
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
        'Is Split Payment',
        related='fiscal_position_id.split_payment')

    @api.one
    @api.depends(
        'invoice_line_ids.price_subtotal', 'tax_line_ids.amount',
        'tax_line_ids.amount_rounding',
        'currency_id', 'company_id', 'date_invoice', 'type'
    )
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        self.amount_sp = 0
        if self.fiscal_position_id.split_payment:
            self.amount_sp = self.amount_tax
            self.amount_total -= self.amount_tax
            self.amount_tax = 0

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
            'date': self.date_invoice,
            'debit': self.amount_sp,
            'credit': 0,
            }
        if self.type == 'out_refund':
            vals['debit'] = 0
            vals['credit'] = self.amount_sp
        return vals

    @api.multi
    def get_receivable_line_ids(self):
        # return the move line ids with the same account as the invoice self
        self.ensure_one()
        return self.move_id.line_ids.filtered(
            lambda r: r.account_id.id == self.account_id.id).ids

    @api.multi
    def _compute_split_payments(self):
        for invoice in self:
            receivable_line_ids = invoice.get_receivable_line_ids()
            move_line_pool = self.env['account.move.line']
            for receivable_line in move_line_pool.browse(receivable_line_ids):
                inv_total = invoice.amount_sp + invoice.amount_total
                if invoice.type == 'out_invoice':
                    if inv_total:
                        receivable_line_amount = (
                            invoice.amount_total * receivable_line.debit
                            ) / inv_total
                    else:
                        receivable_line_amount = 0
                    receivable_line.with_context(
                        check_move_validity=False
                    ).write(
                        {'debit': receivable_line_amount})
                elif invoice.type == 'out_refund':
                    if inv_total:
                        receivable_line_amount = (
                            invoice.amount_total * receivable_line.credit
                            ) / inv_total
                    else:
                        receivable_line_amount = 0
                    receivable_line.with_context(
                        check_move_validity=False
                    ).write(
                        {'credit': receivable_line_amount})

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if invoice.split_payment:
                if invoice.type in ['in_invoice', 'in_refund']:
                    raise UserError(
                        _("Can't handle supplier invoices with split payment"))
                if invoice.move_id.state == 'posted':
                    posted = True
                    invoice.move_id.state = 'draft'
                self._compute_split_payments()
                line_model = self.env['account.move.line']
                write_off_line_vals = invoice._build_debit_line()
                write_off_line_vals['move_id'] = invoice.move_id.id
                line_model.with_context(
                    check_move_validity=False
                ).create(write_off_line_vals)
                if posted:
                    invoice.move_id.state = 'posted'
        return res
