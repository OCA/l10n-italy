# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw
from osv import osv
from tools.translate import _
from decimal import *

class Parser(report_sxw.rml_parse):

    def _get_main_tax(self, tax):
        if not tax.parent_id:
            return tax
        else:
            return self._get_main_tax(tax.parent_id)

    def _get_account_tax(self, inv_tax):
        splitted_name = inv_tax.name.split(' - ')
        if len(splitted_name) > 1:
            tax_name = splitted_name[1]
        else:
            tax_name = splitted_name[0]
        tax_obj = self.pool.get('account.tax')
        # cerco la tassa per nome, dopo averlo ottenuto dalla tassa in fattura
        tax_ids = tax_obj.search(self.cr, self.uid, [('name', '=', tax_name)])
        if not tax_ids:
            raise Exception(_('The tax %s does not exist') % tax_name)
        if len(tax_ids) > 1:
            raise Exception(_('Too many taxes with name %s') % tax_name)
        return tax_obj.browse(self.cr, self.uid, tax_ids[0])

    def _get_tax_lines(self, invoice):
        res=[]
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        totale_iva = 0.0
        totale_iva_inded = 0.0
        precision = self.pool.get('decimal.precision').precision_get(self.cr, self.uid, 'Account')
        for inv_tax in invoice.tax_line:
            tax_item = {}
            if inv_tax.base_code_id and inv_tax.tax_code_id:
                account_tax_amount = self._get_account_tax(inv_tax).amount
                tax_item = {
                    'tax_percentage': account_tax_amount and str(
                        account_tax_amount * 100).split('.')[0] or inv_tax.tax_code_id.name,
                    'base': inv_tax.base,
                    'amount': inv_tax.amount,
                    'non_deductible': 0.0,
                    'index': index,
                    }
                res.append(tax_item)
                totale_iva += inv_tax.amount
                index += 1
            # Se non c'è il tax code imponibile, cerco la tassa relativa alla parte non deducibile
            elif inv_tax.tax_code_id:
                tax = self._get_main_tax(self._get_account_tax(inv_tax))
                for inv_tax_2 in invoice.tax_line:
                    if inv_tax_2.base_code_id and not inv_tax_2.tax_code_id:
                        base_tax = self._get_main_tax(self._get_account_tax(inv_tax_2))
                        # Se hanno la stessa tassa
                        if base_tax.id == tax.id:
                            tax_item = {
                                'tax_percentage': base_tax.amount and str(
                                    base_tax.amount * 100).split('.')[0] or inv_tax.tax_code_id.name,
                                'base': inv_tax.base + inv_tax_2.base,
                                'amount': inv_tax.amount + inv_tax_2.amount,
                                'non_deductible': float(Decimal(str(inv_tax_2.base / (inv_tax.base + inv_tax_2.base) * 100)
                                    ).quantize(Decimal('1.'+precision*'0'), rounding=ROUND_HALF_UP)),
                                'index': index,
                                }
                            res.append(tax_item)
                            totale_iva += inv_tax.amount
                            totale_iva_inded += inv_tax_2.amount
                            index += 1
                            break
            elif not inv_tax.tax_code_id and not inv_tax.base_code_id:
                raise Exception(_('The tax %s has no tax codes') % inv_tax.name)

            if tax_item:
                if tax_item['tax_percentage'] not in self.localcontext['tax_codes']:
                    self.localcontext['tax_codes'][tax_item['tax_percentage']] = {
                        'base': tax_item['base'],
                        'amount': tax_item['amount'],
                        }
                else:
                    self.localcontext['tax_codes'][tax_item['tax_percentage']]['base'] += tax_item['base']
                    self.localcontext['tax_codes'][tax_item['tax_percentage']]['amount'] += tax_item['amount']

        self.localcontext['totali']['totale_operazioni'] += invoice.amount_total
        self.localcontext['totali']['totale_imponibili'] += invoice.amount_untaxed
# da analizzare           self.totale_variazioni += invoice.amount_total
        self.localcontext['totali']['totale_iva'] += totale_iva
        self.localcontext['totali']['totale_iva_inded'] += totale_iva_inded

        return res

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'tax_lines': self._get_tax_lines,
            'totali': {                
                'totale_operazioni': 0.0,
                'totale_imponibili': 0.0,
                'totale_variazioni': 0.0,
                'totale_iva': 0.0,
                'totale_iva_inded': 0.0,
                },
            'tax_codes': {},
        })
