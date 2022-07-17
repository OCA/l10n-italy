# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


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
        if self.e_invoice_line_id and (
            self._context.get('compute_on_einvoice_values', False)
            or self.invoice_id.compute_on_einvoice_values
        ):
            currency = self.invoice_id and self.invoice_id.currency_id or self.\
                company_id.currency_id
            price = self.e_invoice_line_id.unit_price * (
                1 - (self.discount or 0.0) / 100.0)
            subtotal_price = self.e_invoice_line_id.total_price
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

    compute_on_einvoice_values = fields.Boolean(
        readonly=True,
    )

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
                if line.e_invoice_line_id:
                    invoice_line_tax = line.invoice_line_tax_ids[0]
                    if invoice_line_tax not in tax_grouped:
                        tax_grouped.update({invoice_line_tax: {
                            'base': line.e_invoice_line_id.total_price,
                            'amount': 0}}
                        )
                    else:
                        tax_grouped[invoice_line_tax]['base'] += \
                            line.e_invoice_line_id.total_price
                else:
                    invoice_line_tax = line.invoice_line_tax_ids[0]
                    if invoice_line_tax not in tax_grouped:
                        tax_grouped.update({invoice_line_tax: {
                            'base': line.price_subtotal,
                            'amount': 0}}
                        )
                    else:
                        tax_grouped[invoice_line_tax]['base'] += \
                            line.price_subtotal
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
                            [float_round(x['amount'],
                                         precision_rounding=self.currency_id.rounding
                                         ) for x in taxes_recomputed['taxes']])
                        taxes_grouped[key]['amount'] = amount_recomputed
                        taxes_grouped[key]['base'] = sum(
                            [float_round(x['base'],
                                         precision_rounding=self.currency_id.rounding
                                         ) for x in taxes_recomputed['taxes']])
        return taxes_grouped
