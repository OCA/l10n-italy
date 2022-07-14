# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round
import odoo.addons.decimal_precision as dp


class EInvoiceLine(models.Model):
    _inherit = 'einvoice.line'

    unit_price = fields.Float(
        digits=dp.get_precision('Product Price for XML e-invoices')
    )


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    e_invoice_line_id = fields.Many2one(
        'einvoice.line', 'Related E-bill Line', readonly=True)

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id',
                 'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        super()._compute_price()
        # Reset price subtotal to e-invoice value
        if self._context.get('active_model', '') != 'fatturapa.attachment.in' \
                and self.e_invoice_line_id \
                and self.invoice_id.compute_on_einvoice_values:
            currency = self.invoice_id and self.invoice_id.currency_id or self.\
                company_id.currency_id
            round_curr = currency.round
            price = self.e_invoice_line_id.unit_price * (
                1 - (self.discount or 0.0) / 100.0)
            subtotal_price = round_curr(self.e_invoice_line_id.qty * price)
            taxes = False
            if self.invoice_line_tax_ids:
                taxes = self.invoice_line_tax_ids.compute_all(
                    subtotal_price, currency,
                    1,
                    product=self.product_id,
                    partner=self.invoice_id.partner_id)
            self.price_subtotal = price_subtotal_signed = taxes[
                'total_excluded'] if taxes else self.e_invoice_line_id.qty * price
            price_total = taxes['total_included'] if taxes else self.price_subtotal
            taxes_amount = sum(
                [x['amount'] for x in taxes['taxes']]) if taxes else \
                price_total - self.price_subtotal
            self.price_total = self.price_subtotal + taxes_amount
            if self.invoice_id.currency_id and self.invoice_id.currency_id \
                    != self.invoice_id.company_id.currency_id:
                currency = self.invoice_id.currency_id
                date = self.invoice_id._get_currency_rate_date()
                price_subtotal_signed = currency._convert(
                    price_subtotal_signed,
                    self.invoice_id.company_id.currency_id,
                    self.company_id or self.env.user.company_id,
                    date or fields.Date.today())
            sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
            self.price_subtotal_signed = price_subtotal_signed * sign


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    compute_on_einvoice_values = fields.Boolean()

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount',
                 'tax_line_ids.amount_rounding', 'currency_id', 'company_id',
                 'date_invoice', 'type', 'date')
    def _compute_amount(self):
        super()._compute_amount()
        # Compute total and tax on lines price total
        if self._context.get('active_model', '') != 'fatturapa.attachment.in' \
                and self.compute_on_einvoice_values:
            self.amount_untaxed = sum(
                line.price_subtotal for line in self.invoice_line_ids)
            self.amount_total = sum(line.price_total for line in self.invoice_line_ids)
            self.amount_tax = self.amount_total - self.amount_untaxed
            amount_total_company_signed = self.amount_total
            amount_untaxed_signed = self.amount_untaxed
            if self.currency_id and self.company_id and \
                    self.currency_id != self.company_id.currency_id:
                currency_id = self.currency_id
                rate_date = self._get_currency_rate_date() or fields.Date.today()
                amount_total_company_signed = currency_id._convert(
                    self.amount_total, self.company_id.currency_id, self.company_id,
                    rate_date)
                amount_untaxed_signed = currency_id._convert(
                    self.amount_untaxed, self.company_id.currency_id, self.company_id,
                    rate_date)
            sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
            self.amount_total_company_signed = amount_total_company_signed * sign
            self.amount_total_signed = self.amount_total * sign
            self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.multi
    def get_taxes_values(self):
        taxes_grouped = super().get_taxes_values()
        if self.compute_on_einvoice_values:
            tax_grouped = {}
            for line in self.invoice_line_ids:
                if not line.account_id or line.display_type:
                    continue
                if len(line.invoice_line_tax_ids) != 1:
                    continue
                invoice_line_tax = line.invoice_line_tax_ids[0]
                if invoice_line_tax not in tax_grouped:
                    tax_grouped.update({invoice_line_tax: {
                        'base': line.price_subtotal,
                        'amount': 0}}
                    )
                else:
                    tax_grouped[invoice_line_tax]['base'] += line.price_subtotal
            # compute taxes by group
            for key in taxes_grouped:
                for tax_group in tax_grouped:
                    if taxes_grouped[key]['tax_id'] == tax_group.id:
                        taxes_recomputed = tax_group.compute_all(
                            tax_grouped[tax_group]['base'])
                        if any(t.get('price_include', False) for t
                               in taxes_recomputed['taxes']):
                            # no need to do this check for price included taxes
                            continue
                        amount_recomputed = sum(
                            [x['amount'] for x in taxes_recomputed['taxes']])
                        taxes_grouped[key]['amount'] = amount_recomputed
                        taxes_grouped[key]['base'] = float_round(
                            tax_grouped[tax_group]['base'],
                            precision_rounding=self.currency_id.rounding)
        return taxes_grouped
