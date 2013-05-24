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

from osv import fields, osv
import decimal_precision as dp
from decimal import *
import time
from openerp.tools.translate import _

class account_tax(osv.osv):

    _inherit = 'account.tax'

    def _have_same_rate(self, account_taxes):
        rate = None
        for account_tax in account_taxes:
            if rate is None:
                rate = account_tax.amount
            elif rate != account_tax.amount:
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
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.tax_ids))
            return tax_code.tax_ids[0]
        if tax_code.ref_tax_ids:
            if not self._have_same_rate(tax_code.ref_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.ref_tax_ids))
            return tax_code.ref_tax_ids[0]
        raise osv.except_osv(_('Error'),
            _('No taxes associated to tax code %s') % str(tax_code.name))

    def get_account_tax_by_base_code(self, tax_code):
        if tax_code.base_tax_ids:
            if not self._have_same_rate(tax_code.base_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.base_tax_ids))
            return tax_code.base_tax_ids[0]
        if tax_code.ref_base_tax_ids:
            if not self._have_same_rate(tax_code.ref_base_tax_ids):
                raise osv.except_osv(_('Error'),
                    _('The taxes %s have different rates') % str(tax_code.ref_base_tax_ids))
            return tax_code.ref_base_tax_ids[0]
        raise osv.except_osv(_('Error'),
            _('No taxes associated to tax code %s') % str(tax_code.name))

    def compute_all(self, cr, uid, taxes, price_unit, quantity, product=None, partner=None, force_excluded=False):
        res = super(account_tax, self).compute_all(cr, uid, taxes, price_unit, quantity, product, partner, force_excluded)

        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        tax_list = res['taxes']
        totalex = res['total']
        if len(tax_list) == 2:
            for tax in tax_list:
                if tax.get('balance',False): # Calcolo di imponibili per l'IVA parzialmente detraibile
                    deductible_base = totalex
                    ind_tax = tax_list[abs(tax_list.index(tax)-1)]
                    ind_tax_obj = self.browse(cr, uid, ind_tax['id'])
                    ded_tax_obj = self.browse(cr, uid, tax['id'])
                    base_ind = float(Decimal(str(totalex * ind_tax_obj.amount)).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    base_ded = float(Decimal(str(totalex - base_ind)).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    tax_total = float(Decimal(str(tax['balance'])).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    ind_tax['price_unit']  = base_ind
                    tax['price_unit'] = base_ded

        return res

account_tax()

class account_invoice_tax(osv.osv):

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

    def tax_difference(self, cr, uid, cur, tax_grouped):
        real_total = 0
        invoice_total = 0
        cur_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        tax_code_obj = self.pool.get('account.tax.code')
        grouped_base = {}
        for inv_tax in tax_grouped.values():
            if inv_tax['tax_code_id']:
                main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax_by_tax_code(
                    tax_code_obj.browse(cr, uid, inv_tax['tax_code_id'])))
            elif inv_tax['base_code_id']:
                main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax_by_base_code(
                    tax_code_obj.browse(cr, uid, inv_tax['base_code_id'])))
            else:
                raise osv.except_osv(_('Error'),
                    _('No tax codes for invoice tax %s') % inv_tax['name'])
            if not grouped_base.get(main_tax.amount, False):
                grouped_base[main_tax.amount] = 0
            grouped_base[main_tax.amount] +=  inv_tax['base']
        for tax_rate in grouped_base:
            real_total += grouped_base[tax_rate] * tax_rate
        real_total = cur_obj.round(cr, uid, cur, real_total)
        for inv_tax in tax_grouped.values():
            invoice_total += inv_tax['amount']
        return real_total - invoice_total

    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context)
        inv_obj = self.pool.get('account.invoice')
        tax_obj = self.pool.get('account.tax')
        tax_code_obj = self.pool.get('account.tax.code')
        invoice = inv_obj.browse(cr, uid, invoice_id, context=context)
        cur = invoice.currency_id
        tax_difference = self.tax_difference(cr, uid, cur, tax_grouped)
        cur_obj = self.pool.get('res.currency')
        if cur_obj.is_zero(cr, uid, cur, tax_difference):
            return tax_grouped
        company_currency = invoice.company_id.currency_id.id
        for inv_tax in tax_grouped.values():
            # parte detraibile
            if not inv_tax['base_code_id'] and inv_tax['tax_code_id']:
                ded_tax = tax_obj.get_account_tax_by_tax_code(
                    tax_code_obj.browse(cr, uid, inv_tax['tax_code_id']))
                tax = tax_obj.get_main_tax(ded_tax)
                for inv_tax_2 in tax_grouped.values():
                    # parte indetraibile
                    if inv_tax_2['base_code_id'] and not inv_tax_2['tax_code_id']:
                        main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax_by_base_code(
                            tax_code_obj.browse(cr, uid, inv_tax_2['base_code_id'])))
                        # Se hanno la stessa tassa
                        # (Il get_account_tax_by* potrebbe in generale ritornare una qualunque
                        # delle N imposte associate al tax_code. Per la parte indetraibile, il
                        # tax code dovrà sempre avere una sola imposta)
                        if main_tax.id == tax.id:
                            # se risulta un'eccedenza, la tolgo dalla parte detraibile
                            if tax_difference < 0:
                                inv_tax['amount'] = inv_tax['amount'] + tax_difference
                            # se risulta una mancanza, la aggiungo alla parte indetraibile
                            elif tax_difference > 0:
                                inv_tax_2['amount'] = inv_tax_2['amount'] + tax_difference
                            # calcolo l'importo del tax.code relativo all'imposta (la parte indetraibile non lo muove)
                            if invoice.type in ('out_invoice','in_invoice'):
                                inv_tax['tax_amount'] = cur_obj.compute(cr, uid, invoice.currency_id.id, company_currency,
                                    inv_tax['amount'] * main_tax['tax_sign'],
                                    context={'date': invoice.date_invoice or time.strftime('%Y-%m-%d')}, round=False)
                            else:
                                inv_tax['tax_amount'] = cur_obj.compute(cr, uid, invoice.currency_id.id, company_currency,
                                    inv_tax['amount'] * main_tax['ref_tax_sign'],
                                    context={'date': invoice.date_invoice or time.strftime('%Y-%m-%d')}, round=False)

                            inv_tax['amount'] = cur_obj.round(cr, uid, cur, inv_tax['amount'])
                            inv_tax['tax_amount'] = cur_obj.round(cr, uid, cur, inv_tax['tax_amount'])
                            inv_tax_2['amount'] = cur_obj.round(cr, uid, cur, inv_tax_2['amount'])
        return tax_grouped


class account_tax_code(osv.osv):

    _inherit = 'account.tax.code'

    _columns = {
        'base_tax_ids': fields.one2many('account.tax', 'base_code_id', 'Base Taxes'),
        'tax_ids': fields.one2many('account.tax', 'tax_code_id', 'Taxes'),
        'ref_base_tax_ids': fields.one2many('account.tax', 'ref_base_code_id', 'Ref Base Taxes'),
        'ref_tax_ids': fields.one2many('account.tax', 'ref_tax_code_id', 'Ref Taxes'),
        }
