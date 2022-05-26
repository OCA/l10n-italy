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

    @api.multi
    def get_receivable_line_ids(self):
        # return the move line ids with the same account as the invoice self
        self.ensure_one()
        return self.move_id.line_ids.filtered(
            lambda r: r.account_id.id == self.account_id.id).ids

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        total, total_currency, iml = \
            super(AccountInvoice, self).compute_invoice_totals(
                company_currency, invoice_move_lines)

        if self.split_payment:
            if self.type in ['in_invoice', 'in_refund']:
                raise UserError(_("Can't handle supplier invoices with split payment"))

            sign = 1 if self.type == 'out_invoice' else -1

            amount_sp = sign * self.amount_sp
            total -= amount_sp

            diff_currency = self.currency_id != company_currency
            amount_sp_currency = company_currency._convert(
                amount_sp, self.currency_id, self.company_id, 
                self._get_currency_rate_date() or fields.Date.today())

            iml.append({
                'type': 'dest',
                'name': _('Split Payment Write Off'),
                'price': amount_sp,
                'account_id': self.company_id.sp_account_id.id,
                'date_maturity': self.date_invoice,
                'amount_currency': diff_currency and amount_sp_currency,
                'currency_id': diff_currency and self.currency_id.id,
                'invoice_id': self.id
            })

        return total, total_currency, iml
