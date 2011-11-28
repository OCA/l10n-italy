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
        total = 0.0
        if not move_line.credit:
            for line in move_line.move_id.line_id:
                if line.credit and not line.tax_code_id:
                    total += line.credit
        elif not move_line.debit:
            for line in move_line.move_id.line_id:
                if line.debit and not line.tax_code_id:
                    total +=  line.debit
        return total

    # Calcola il segno corretto sulla base del tax code.
    # Il tax code ha l'importo in valuta base, ma ha segno negativo per l'IVA a credito (da stampare positiva)
    # e per le note di credito (da stampare positive)
    def _get_amount_with_sign(self, tax_code_amount, amount):
        return abs(tax_code_amount) * cmp(amount, 0)
    
    # in valuta base
    def _get_invoice_amount_total(self, invoice):
        total = 0.0
        for inv_tax in invoice.tax_line:
            total += self._get_amount_with_sign(inv_tax.base_amount, inv_tax.base) \
                + self._get_amount_with_sign(inv_tax.tax_amount, inv_tax.amount)
        return total
    
    # in valuta base
    def _get_invoice_amount_untaxed(self, invoice):
        total = 0.0
        for inv_tax in invoice.tax_line:
            total += self._get_amount_with_sign(inv_tax.base_amount, inv_tax.base)
        return total

    def _get_tax_lines_by_invoice(self, invoice):
        res=[]
        tax_obj = self.pool.get('account.tax')
        cur_pool = self.pool.get('res.currency')
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        totale_iva = 0.0
        totale_iva_inded = 0.0
        invoice_amount_total = 0.0
        invoice_amount_untaxed = 0.0
        precision = self.pool.get('decimal.precision').precision_get(self.cr, self.uid, 'Account')
        for inv_tax in invoice.tax_line:
            tax_item = {}
            if inv_tax.base_code_id and inv_tax.tax_code_id:
                account_tax = tax_obj.get_account_tax(self.cr, self.uid, inv_tax.name)
                if account_tax.exclude_from_registries:
                    self.logger.notifyChannel("l10n_it_vat_registries", netsvc.LOG_INFO,
                        _('The tax %s is excluded from registries') % account_tax.name)
                    continue
                account_tax_amount = account_tax.amount
                invoice_amount_total = self._get_invoice_amount_total(invoice)
                invoice_amount_untaxed = self._get_invoice_amount_untaxed(invoice)
                amount = self._get_amount_with_sign(inv_tax.tax_amount, inv_tax.amount)
                base = self._get_amount_with_sign(inv_tax.base_amount, inv_tax.base)
                tax_item = {
                    'tax_percentage': account_tax_amount and str(
                        account_tax_amount * 100).split('.')[0] or inv_tax.tax_code_id.name,
                    'base': base,
                    'amount': amount, #in valuta base
                    'non_deductible': 0.0,
                    'index': index,
                    'amount_total': invoice_amount_total,
                    }
                res.append(tax_item)
                totale_iva += amount
                index += 1
            # Se non c'è il tax code imponibile, cerco la tassa relativa alla parte non deducibile
            elif inv_tax.tax_code_id:
                tax = tax_obj.get_main_tax(tax_obj.get_account_tax(self.cr, self.uid, inv_tax.name))
                if tax.exclude_from_registries:
                    self.logger.notifyChannel("l10n_it_vat_registries", netsvc.LOG_INFO,
                        _('The tax %s is excluded from registries') % tax.name)
                    continue
                for inv_tax_2 in invoice.tax_line:
                    if inv_tax_2.base_code_id and not inv_tax_2.tax_code_id:
                        base_tax = tax_obj.get_main_tax(tax_obj.get_account_tax(self.cr, self.uid, inv_tax_2.name))
                        # Se hanno la stessa tassa
                        if base_tax.id == tax.id:
                            non_deductible = (inv_tax_2.base_amount / (inv_tax.base_amount + inv_tax_2.base_amount) * 100)
                            invoice_amount_total = self._get_invoice_amount_total(invoice)
                            invoice_amount_untaxed = self._get_invoice_amount_untaxed(invoice)
                            amount = self._get_amount_with_sign(inv_tax.tax_amount, inv_tax.amount)
                            base = self._get_amount_with_sign(inv_tax.base_amount, inv_tax.base)
                            amount2 = self._get_amount_with_sign(inv_tax_2.tax_amount, inv_tax_2.amount)
                            base2 = self._get_amount_with_sign(inv_tax_2.base_amount, inv_tax_2.base)
                            tax_item = {
                                'tax_percentage': base_tax.amount and str(
                                    base_tax.amount * 100).split('.')[0] or inv_tax.tax_code_id.name,
                                'base': base + base2,
                                'amount': amount + amount2,
                                'non_deductible': non_deductible and str(non_deductible).split('.')[0] or '',
                                'index': index,
                                'amount_total': invoice_amount_total,
                                }
                            res.append(tax_item)
                            totale_iva += amount
                            totale_iva_inded += amount2
                            index += 1
                            break
            elif not inv_tax.tax_code_id and not inv_tax.base_code_id:
                self.logger.notifyChannel("l10n_it_vat_registries", netsvc.LOG_INFO,
                    _('The tax %s has no tax codes') % inv_tax.name)
                continue
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

    def _get_tax_lines(self, move):
        res=[]
        tax_obj = self.pool.get('account.tax')
        cur_pool = self.pool.get('res.currency')
        inv_pool = self.pool.get('account.invoice')
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        totale_iva = 0.0
        totale_iva_inded = 0.0
        invoice_amount_total = 0.0
        invoice_amount_untaxed = 0.0
        related_invoices = []
        
        # se c'è l'oggetto fattura, utilizzo il calcolo su fattura
        for move_line in move.line_id:
            if move_line.invoice and move_line.invoice.id not in related_invoices:
                related_invoices.append(move_line.invoice.id)
        if related_invoices:
            for invoice_id in related_invoices:
                return self._get_tax_lines_by_invoice(inv_pool.browse(self.cr, self.uid, invoice_id))
                
        for move_line in move.line_id:
            tax_item = {}
            if move_line.tax_code_id and move_line.tax_code_id.tax_ids:
                main_tax = tax_obj.get_main_tax(move_line.tax_code_id.tax_ids[0])
                if main_tax.exclude_from_registries:
                    self.logger.notifyChannel("l10n_it_vat_registries", netsvc.LOG_INFO,
                        _('The tax %s is excluded from registries') % main_tax.name)
                    continue
                # sommo gli imponibili relativi all'imposta corrente
                base_amount = 0.0
                for line in move_line.move_id.line_id:
                    if line.tax_code_id.id == main_tax.base_code_id.id:
                        base_amount += self._get_amount_with_sign(line.tax_amount, line.debit - line.credit)
                # calcolo % indetraibile
                actual_tax_amount = base_amount * main_tax.amount
                actual_tax_amount = cur_pool.round(self.cr, self.uid, move.company_id.currency_id, actual_tax_amount)
                non_deductible = 0.0
                if abs(actual_tax_amount) != abs(move_line.tax_amount):
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
