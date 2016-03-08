# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api, _
from decimal import Decimal, ROUND_HALF_UP
from openerp.exceptions import Warning


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _have_same_rate(self, account_taxes):
        rate = None
        for acc_tax in account_taxes:
            if acc_tax.type != 'balance':
                if rate is None:
                    rate = acc_tax.amount
                elif rate != acc_tax.amount:
                    return False
        return True

    def get_main_tax(self, tax):
        if not tax.parent_id:
            return tax
        else:
            return self.get_main_tax(tax.parent_id)

    def get_account_tax_by_tax_code(self, tax_code):
        if tax_code.tax_ids:
            if not self._have_same_rate(tax_code.tax_ids):
                raise Warning(_('The taxes %s have different rates') % str(
                    tax_code.tax_ids))
            return tax_code.tax_ids[0]
        if tax_code.ref_tax_ids:
            if not self._have_same_rate(tax_code.ref_tax_ids):
                raise Warning(_('The taxes %s have different rates') % str(
                    tax_code.ref_tax_ids))
            return tax_code.ref_tax_ids[0]
        raise Warning(_('No taxes associated to tax code %s') % str(
            tax_code.name))

    def get_account_tax_by_base_code(self, tax_code):
        if tax_code.base_tax_ids:
            if not self._have_same_rate(tax_code.base_tax_ids):
                raise Warning(_('The taxes %s have different rates') % str(
                    tax_code.base_tax_ids))
            return tax_code.base_tax_ids[0]
        if tax_code.ref_base_tax_ids:
            if not self._have_same_rate(tax_code.ref_base_tax_ids):
                raise Warning(_('The taxes %s have different rates') % str(
                    tax_code.ref_base_tax_ids))
            return tax_code.ref_base_tax_ids[0]
        raise Warning(_('No taxes associated to tax code %s') % str(
            tax_code.name))

    @api.v7
    def compute_all(self, cr, uid, taxes, price_unit, quantity, product=None,
                    partner=None, force_excluded=False):
        '''
        Modify compute_all function in order to put correct total in case of
        tax with one child (usually partially deductible)'''

        res = super(AccountTax, self).compute_all(
            cr, uid, taxes, price_unit, quantity, product=product,
            partner=partner, force_excluded=force_excluded)
        precision = 2  # always 2 even if changed in 'Account' precision
        # self.pool['decimal.precision'].precision_get(cr, uid, 'Account')
        tax_list = res['taxes']
        totalex = res['total']
        if len(tax_list) == 2:
            for tax in tax_list:
                if tax.get('balance', False):
                    ind_tax = tax_list[abs(tax_list.index(tax) - 1)]
                    ind_tax_obj = self.browse(cr, uid, ind_tax['id'])
                    base_ind = float(
                        Decimal(str(totalex * ind_tax_obj.amount)).quantize(
                            Decimal('1.' + precision * '0'),
                            rounding=ROUND_HALF_UP))
                    base_ded = float(
                        Decimal(str(totalex - base_ind)).quantize(
                            Decimal('1.' + precision * '0'),
                            rounding=ROUND_HALF_UP))
                    tax_total = float(Decimal(str(tax['balance'])).quantize(
                        Decimal('1.' + precision * '0'),
                        rounding=ROUND_HALF_UP))
                    if tax_total > tax['amount'] + ind_tax['amount']:
                        rounding_amount = tax_total - (tax['amount'] +
                                                       ind_tax['amount'])
                        ind_tax['amount'] += rounding_amount
                    ind_tax['price_unit'] = round(
                        base_ind / quantity,
                        self.pool['decimal.precision'].precision_get(
                            cr, uid, 'Product Price'))
                    tax['price_unit'] = round(
                        base_ded / quantity,
                        self.pool['decimal.precision'].precision_get(
                            cr, uid, 'Product Price'))
        return res

    @api.v8
    def compute_all(self, price_unit, quantity, product=None, partner=None,
                    force_excluded=False):
        return self._model.compute_all(
            self._cr, self._uid, self, price_unit, quantity,
            product=product, partner=partner, force_excluded=force_excluded)


class AccountInvoiceTax(models.Model):

    _inherit = "account.invoice.tax"

    '''
    tax_grouped:

    {(False, 21, 132): {'account_id': 132,
                    'amount': 12.36,
                    'base': 61.79,
                    'base_amount': 61.79,
                    'base_code_id': 21,
                    'invoice_id': 1L,
                    'manual': False,
                    'name': u'20I5b - IVA al 20% detraibile al 50% (I)',
                    'sequence': 1,
                    'tax_amount': 12.36,
                    'tax_code_id': False},
    (20, False, 46): {'account_id': 46,
                   'amount': 12.35,
                   'base': 61.78,
                   'base_amount': 61.78,
                   'base_code_id': False,
                   'invoice_id': 1L,
                   'manual': False,
                   'name': u'20I5a - IVA al 20% detraibile al 50% (D)',
                   'sequence': 2,
                   'tax_amount': 12.35,
                   'tax_code_id': 20},
    (26, 27, 46): {'account_id': 46,
                'amount': 24.71,
                'base': 123.57000000000001,
                'base_amount': 123.57000000000001,
                'base_code_id': 27,
                'invoice_id': 1L,
                'manual': False,
                'name': u'20b - Iva al 20% (credito)',
                'sequence': 1,
                'tax_amount': 24.71,
                'tax_code_id': 26}}
    '''
    @api.model
    def tax_difference(self, cur, tax_grouped):
        real_total = 0
        invoice_total = 0
        tax_obj = self.env['account.tax']
        tax_code_obj = self.env['account.tax.code']
        grouped_base = {}
        for inv_tax in tax_grouped.values():
            if inv_tax['tax_code_id']:
                main_tax = tax_obj.get_main_tax(
                    tax_obj.get_account_tax_by_tax_code(
                        tax_code_obj.browse(inv_tax['tax_code_id'])))
            elif inv_tax['base_code_id']:
                main_tax = tax_obj.get_main_tax(
                    tax_obj.get_account_tax_by_base_code(
                        tax_code_obj.browse(inv_tax['base_code_id'])))
            else:
                raise Warning(
                    _('No tax codes for invoice tax %s') % inv_tax['name'])
            if not grouped_base.get(main_tax.amount, False):
                grouped_base[main_tax.amount] = 0
            grouped_base[main_tax.amount] += inv_tax['base']
        for tax_rate in grouped_base:
            real_total += grouped_base[tax_rate] * tax_rate
        real_total = cur.round(real_total)
        for inv_tax in tax_grouped.values():
            invoice_total += inv_tax['amount']
        return real_total - invoice_total

    @api.v8
    def compute(self, invoice):
        tax_grouped = super(AccountInvoiceTax, self).compute(invoice)
        tax_obj = self.env['account.tax']
        tax_code_obj = self.env['account.tax.code']
        cur = invoice.currency_id.with_context(
            date=invoice.date_invoice or fields.Date.context_today(invoice))
        tax_difference = self.tax_difference(cur, tax_grouped)
        if cur.is_zero(tax_difference):
            return tax_grouped
        company_currency = invoice.company_id.currency_id
        for inv_tax in tax_grouped.values():
            # parte detraibile
            if not inv_tax['base_code_id'] and inv_tax['tax_code_id']:
                ded_tax = tax_obj.get_account_tax_by_tax_code(
                    tax_code_obj.browse(inv_tax['tax_code_id']))
                tax = tax_obj.get_main_tax(ded_tax)
                for inv_tax_2 in tax_grouped.values():
                    # parte indetraibile
                    if inv_tax_2[
                        'base_code_id'
                    ] and not inv_tax_2[
                        'tax_code_id'
                    ]:
                        main_tax = tax_obj.get_main_tax(
                            tax_obj.get_account_tax_by_base_code(
                                tax_code_obj.browse(
                                    inv_tax_2['base_code_id'])))
                        # Se hanno la stessa tassa (Il get_account_tax_by*
                        # potrebbe in generale ritornare una qualunque
                        # delle N imposte associate al tax_code.
                        # Per la parte indetraibile, il
                        # tax code dovrà sempre avere una sola imposta)
                        if main_tax.id == tax.id:
                            # se risulta un'eccedenza, la tolgo dalla parte
                            # detraibile
                            if tax_difference < 0:
                                inv_tax['amount'] = inv_tax[
                                    'amount'] + tax_difference
                            # se risulta una mancanza, la aggiungo alla parte
                            # indetraibile
                            elif tax_difference > 0:
                                inv_tax_2['amount'] = inv_tax_2[
                                    'amount'] + tax_difference
                            # calcolo l'importo del tax.code relativo all'
                            # imposta (la parte indetraibile non lo muove)
                            if invoice.type in ('out_invoice', 'in_invoice'):
                                inv_tax[
                                    'tax_amount'
                                ] = cur.with_context(
                                    date=invoice.date_invoice or
                                    fields.Date.context_today(invoice)).\
                                    compute(
                                    inv_tax['amount'] * main_tax['tax_sign'],
                                    company_currency,
                                    round=False)
                            else:
                                inv_tax['tax_amount'] = cur.with_context(
                                    date=invoice.date_invoice or
                                    fields.Date.context_today(invoice)).\
                                    compute(inv_tax['amount'] *
                                            main_tax['ref_tax_sign'],
                                            company_currency,
                                            round=False)

                            inv_tax['amount'] = cur.round(inv_tax['amount'])
                            inv_tax['tax_amount'] = cur.round(
                                inv_tax['tax_amount'])
                            inv_tax_2['amount'] = cur.round(
                                inv_tax_2['amount'])
        return tax_grouped

    @api.v7
    def compute(self, cr, uid, invoice_id, context=None):
        recs = self.browse(cr, uid, [], context)
        invoice = recs.env['account.invoice'].browse(invoice_id)
        return recs.compute(invoice)


class AccountTaxCode(models.Model):

    _inherit = 'account.tax.code'

    base_tax_ids = fields.One2many('account.tax', 'base_code_id', 'Base Taxes')
    tax_ids = fields.One2many('account.tax', 'tax_code_id', 'Taxes')
    ref_base_tax_ids = fields.One2many(
        'account.tax', 'ref_base_code_id', 'Ref Base Taxes')
    ref_tax_ids = fields.One2many(
        'account.tax', 'ref_tax_code_id', 'Ref Taxes')


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    @api.model
    def move_line_get(self, invoice_id):
        inv = self.env['account.invoice'].browse(invoice_id)
        currency = inv.currency_id.with_context(date=inv.date_invoice)
        company_currency = inv.company_id.currency_id
        res = []
        for line in inv.invoice_line:
            mres = self.move_line_get_item(line)
            mres['invl_id'] = line.id
            res.append(mres)
            tax_code_found = False
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, inv.partner_id)['taxes']
            for tax in taxes:
                if inv.type in ('out_invoice', 'in_invoice'):
                    tax_code_id = tax['base_code_id']
                    # Changed for https://github.com/OCA/OCB/commit/
                    # d83befdb0f4cdc34f1d2aad7f91f07efe7d3bccf
                    # Else it would put a wrong amount in base tax
                    if self.env['account.tax'].browse(
                            tax['id']).include_base_amount:
                        tax_amount = tax['price_unit'] * line.quantity * \
                            tax['base_sign']
                    else:
                        tax_amount = line.price_subtotal * tax['base_sign']
                else:
                    tax_code_id = tax['ref_base_code_id']
                    if self.env['account.tax'].browse(
                            tax['id']).include_base_amount:
                        tax_amount = tax['price_unit'] * line.quantity * \
                            tax['ref_base_sign']
                    else:
                        tax_amount = line.price_subtotal * tax['base_sign']
                    # End change

                if tax_code_found:
                    if not tax_code_id:
                        continue
                    res.append(dict(mres))
                    res[-1]['price'] = 0.0
                    res[-1]['account_analytic_id'] = False
                elif not tax_code_id:
                    continue
                tax_code_found = True

                res[-1]['tax_code_id'] = tax_code_id
                res[-1]['tax_amount'] = currency.compute(
                    tax_amount, company_currency)

        return res
