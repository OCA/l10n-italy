# -*- coding: utf-8 -*-
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
import netsvc

class Parser(report_sxw.rml_parse):

    logger = netsvc.Logger()
    
    def _move_total(self, move_line):
        if not move_line.credit:
            for line in move_line.move_id.line_id:
                if line.credit:
                    return line.credit
        elif not move_line.debit:
            for line in move_line.move_id.line_id:
                if line.debit:
                    return line.debit

    def _get_tax_lines(self, move):
        res=[]
        tax_obj = self.pool.get('account.tax')
        cur_pool = self.pool.get('res.currency')
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        totale_iva = 0.0
        totale_iva_inded = 0.0
        invoice_amount_total = 0.0
        invoice_amount_untaxed = 0.0
        for move_line in move.line_id:
            tax_item = {}
            if move_line.tax_code_id and move_line.tax_code_id.tax_ids:
                main_tax = tax_obj.get_main_tax(move_line.tax_code_id.tax_ids[0])
                # sommo gli imponibili relativi all'imposta corrente
                base_amount = 0.0
                for line in move_line.move_id.line_id:
                    if line.tax_code_id.id == main_tax.base_code_id.id:
                        base_amount += line.tax_amount
                # calcolo % indetraibile
                actual_tax_amount = base_amount * main_tax.amount
                actual_tax_amount = cur_pool.round(self.cr, self.uid, move.company_id.currency_id, actual_tax_amount)
                non_deductible = 0.0
                if actual_tax_amount != move_line.tax_amount:
                    non_deductible = 100
                    if move_line.tax_amount:
                        non_deductible = 100 - abs((move_line.tax_amount * 100.0) / actual_tax_amount)
                        non_deductible = cur_pool.round(self.cr, self.uid, move.company_id.currency_id, non_deductible)
                # calcolo il totale dell'operazione
                invoice_amount_total = self._move_total(move_line)
                if base_amount < 0:
                    invoice_amount_total = - invoice_amount_total
                tax_item = {
                    'tax_percentage': main_tax.amount and str(
                        main_tax.amount * 100).split('.')[0] or move_line.tax_code_id.name,
                    'base': base_amount,
                    'amount': actual_tax_amount,
                    'non_deductible': non_deductible and str(non_deductible).split('.')[0] or '',
                    'index': index,
                    'amount_total': invoice_amount_total,
                    }
                res.append(tax_item)
                totale_iva += cur_pool.round(self.cr, self.uid, move.company_id.currency_id,
                    (actual_tax_amount * (100 - non_deductible) * 0.01))
                invoice_amount_untaxed += base_amount
                totale_iva_inded += cur_pool.round(self.cr, self.uid, move.company_id.currency_id,
                    (actual_tax_amount * non_deductible * 0.01))
                index += 1

            if tax_item:
                if tax_item['tax_percentage'] not in self.localcontext['tax_codes']:
                    self.localcontext['tax_codes'][tax_item['tax_percentage']] = {
                        'base': tax_item['base'],
                        'amount': tax_item['amount'],
                        }
                else:
                    self.localcontext['tax_codes'][tax_item['tax_percentage']]['base'] += tax_item['base']
                    self.localcontext['tax_codes'][tax_item['tax_percentage']]['amount'] += tax_item['amount']

        self.localcontext['totali']['totale_operazioni'] += invoice_amount_total
        self.localcontext['totali']['totale_imponibili'] += invoice_amount_untaxed
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

        
report_sxw.report_sxw('report.registro_iva_vendite',
                       'registro_iva_vendite', 
                       'addons/l10n_it_vat_registries/templates/registro_iva_vendite.mako',
                       parser=Parser)
report_sxw.report_sxw('report.registro_iva_acquisti',
                       'registro_iva_acquisti', 
                       'addons/l10n_it_vat_registries/templates/registro_iva_acquisti.mako',
                       parser=Parser)
report_sxw.report_sxw('report.registro_iva_corrispettivi',
                       'registro_iva_corrispettivi', 
                       'addons/l10n_it_vat_registries/templates/registro_iva_corrispettivi.mako',
                       parser=Parser)
