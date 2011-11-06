# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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

class account_tax(osv.osv):

    _inherit = 'account.tax'

    def compute_all(self, cr, uid, taxes, price_unit, quantity, address_id=None, product=None, partner=None):
        res = super(account_tax, self).compute_all(cr, uid, taxes, price_unit, quantity, address_id, product, partner)
        
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        tax_list = res['taxes']
        totalex = res['total']
        if len(tax_list) == 2:
            for tax in tax_list:
                if tax.get('balance',False): # Calcolo di imponibili e imposte per l'IVA parzialmente detraibile
                    deductible_base = totalex
                    ind_tax = tax_list[abs(tax_list.index(tax)-1)]
                    ind_tax_obj = self.browse(cr, uid, ind_tax['id'])
                    ded_tax_obj = self.browse(cr, uid, tax['id'])
                    base_ind = float(Decimal(str(totalex * ind_tax_obj.amount)).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    base_ded = float(Decimal(str(totalex - base_ind)).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    tax_total = float(Decimal(str(tax['balance'])).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    #tax_ind = float(Decimal(str(tax_total * ind_tax_obj.amount)).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP))
                    #tax_ded = tax_total - tax_ind
                    ind_tax['price_unit']  = base_ind
                    tax['price_unit'] = base_ded
                    # account_invoice_tax_by_column li sovrascrive
                    #ind_tax['amount']  = tax_ind
                    #tax['amount'] = tax_ded

        return res

account_tax()

class account_invoice_tax(osv.osv):

    _inherit = "account.invoice.tax"
    
    '''
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
    
    def tax_differ(self, cr, uid, cur, tax_grouped):
        real_total = 0
        invoice_total = 0
        cur_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        grouped_base = {}
        for inv_tax in tax_grouped.values():
            main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax(cr, uid, inv_tax['name']))
            if not grouped_base.get(main_tax.amount, False):
                grouped_base[main_tax.amount] = 0
            grouped_base[main_tax.amount] +=  inv_tax['base']
        for tax_rate in grouped_base:
            real_total += grouped_base[tax_rate] * tax_rate
        real_total = cur_obj.round(cr, uid, cur, real_total)
        for inv_tax in tax_grouped.values():
            invoice_total += inv_tax['amount']
        if cur_obj.is_zero(cr, uid, cur, (real_total - invoice_total)):
            return False
        else:
            return True

    def compute(self, cr, uid, invoice_id, context=None):
        tax_grouped = super(account_invoice_tax, self).compute(cr, uid, invoice_id, context)
        inv_obj = self.pool.get('account.invoice')
        tax_obj = self.pool.get('account.tax')
        invoice = inv_obj.browse(cr, uid, invoice_id, context=context)
        cur = invoice.currency_id
        import pdb;pdb.set_trace()
        if not self.tax_differ(cr, uid, cur, tax_grouped):
            return tax_grouped
        company_currency = invoice.company_id.currency_id.id
        cur_obj = self.pool.get('res.currency')
        for inv_tax in tax_grouped.values():
            # parte detraibile
            if not inv_tax['base_code_id'] and inv_tax['tax_code_id']:
                ded_tax = tax_obj.get_account_tax(cr, uid, inv_tax['name'])
                tax = tax_obj.get_main_tax(ded_tax)
                for inv_tax_2 in tax_grouped.values():
                    # parte indetraibile
                    if inv_tax_2['base_code_id'] and not inv_tax_2['tax_code_id']:
                        main_tax = tax_obj.get_main_tax(tax_obj.get_account_tax(cr, uid, inv_tax_2['name']))
                        # Se hanno la stessa tassa
                        if main_tax.id == tax.id:
                            total_base = inv_tax['base_amount'] + inv_tax_2['base_amount']
                            total_tax = cur_obj.round(cr, uid, cur, total_base * tax.amount)
                            total_inv_tax = inv_tax['amount'] + inv_tax_2['amount']
                            if not cur_obj.is_zero(cr, uid, cur, (total_tax - total_inv_tax)):
                                # se risulta un'eccedenza, la tolgo dalla parte detraibile
                                if total_tax < total_inv_tax:
                                    inv_tax['amount'] = inv_tax['amount'] - (total_inv_tax - total_tax)
                                # se risulta una mancanza, la aggiungo alla parte indetraibile
                                elif total_tax > total_inv_tax:
                                    inv_tax_2['amount'] = inv_tax_2['amount'] + (total_tax - total_inv_tax)
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
    
account_invoice_tax()
