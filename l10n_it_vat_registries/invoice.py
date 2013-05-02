# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import time
from report import report_sxw
from tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class Parser(report_sxw.rml_parse):
    
    def _get_partner_type_by_move(self, move):
        partner_type = ''
        for line in move.line_id:
            if line.account_id.type == 'payable' or line.account_id.type == 'receivable':
                if not partner_type:
                    partner_type = line.account_id.type
                elif partner_type != line.account_id.type:
                    raise Exception(
                        _('The move %s has different partner account type') % move.name)
        return partner_type

    def _get_partner_type(self, move_line):
        return self._get_partner_type_by_move(move_line.move_id)

    def _move_total(self, move_line):
        partner_type = self._get_partner_type(move_line)
        total = 0.0
        for line in move_line.move_id.line_id:
            if line.account_id.type == partner_type:
                total += (line.debit or line.credit)
        return total

    # Metto al tax code il segno dell'importo dell'imposta.
    # Il tax code ha l'importo in valuta base, ma ha segno negativo per l'IVA a credito (da stampare positiva)
    # e per le note di credito (da stampare negative)
    def _get_amount_with_sign(self, tax_code_amount, amount):
        return abs(tax_code_amount) * cmp(amount, 0)

    def _is_refund(self, move_line):
        if self._get_partner_type(move_line) == 'receivable' and move_line.debit > move_line.credit:
            return True
        if self._get_partner_type(move_line) == 'payable' and move_line.debit < move_line.credit:
            return True

    def _get_line_amount_with_sign(self, move_line):
        if self._get_partner_type(move_line) == 'receivable':
            return self._get_amount_with_sign(move_line.tax_amount, move_line.credit - move_line.debit)
        if self._get_partner_type(move_line) == 'payable':
            return self._get_amount_with_sign(move_line.tax_amount, move_line.debit - move_line.credit)

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

    def _get_tax_lines(self, move):
        res=[]
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0

        for move_line in move.line_id:
            tax_item = {}
            if move_line.tax_code_id and move_line.tax_code_id.tax_ids:
                # Nel wizard ho già controllato che le eventuali diverse
                # imposte abbiamo la stessa aliquota.
                # Le diverse imposte devono comunque usare gli stessi tax code
                main_tax = tax_obj.get_main_tax(move_line.tax_code_id.tax_ids[0])
                if main_tax.exclude_from_registries:
                    _logger.info(_('The tax %s is excluded from registries') % main_tax.name)
                    continue
                # sommo gli imponibili relativi all'imposta corrente
                base_amount = 0.0
                for line in move_line.move_id.line_id:
                    if line.tax_code_id.id == main_tax.base_code_id.id:
                        base_amount += self._get_line_amount_with_sign(line)
                if base_amount and main_tax.amount:
                    actual_tax_amount = base_amount * main_tax.amount
                else:
                    actual_tax_amount = move_line.tax_amount
                actual_tax_amount = cur_pool.round(
                    self.cr, self.uid, move.company_id.currency_id,
                    actual_tax_amount)
                # calcolo % indetraibile
                non_deductible = 0.0
                if abs(actual_tax_amount) != abs(move_line.tax_amount):
                    non_deductible = 100
                    if move_line.tax_amount:
                        non_deductible = 100 - abs((
                            move_line.tax_amount * 100.0) / actual_tax_amount)
                        non_deductible = cur_pool.round(
                            self.cr, self.uid, move.company_id.currency_id,
                            non_deductible)
                # calcolo il totale dell'operazione
                invoice_amount_total = self._move_total(move_line)
                if self._is_refund(move_line):
                    invoice_amount_total = - invoice_amount_total
                str_non_deductible = str(non_deductible).split('.')[0]
                tax_item = {
                    'tax_percentage': main_tax.amount and str(
                        main_tax.amount * 100).split('.')[0] or
                        move_line.tax_code_id.name,
                    'tax_code_name': move_line.tax_code_id.name,
                    'base': base_amount,
                    'amount': actual_tax_amount,
                    'non_deductible': str_non_deductible != '0' and
                        str_non_deductible or '',
                    'index': index,
                    'amount_total': invoice_amount_total,
                    'invoice_date': (move_line.invoice and move_line.invoice.date_invoice
                        or move_line.date or ''),
                    }
                res.append(tax_item)
                iva = cur_pool.round(
                    self.cr, self.uid, move.company_id.currency_id,
                    (actual_tax_amount * (100 - non_deductible) * 0.01))
                iva_inded = cur_pool.round(
                    self.cr, self.uid, move.company_id.currency_id,
                    (actual_tax_amount * non_deductible * 0.01))
                tax_difference= (iva + iva_inded) - actual_tax_amount
                # se risulta un'eccedenza, la tolgo dalla parte detraibile
                if tax_difference > 0:
                    iva = iva - tax_difference
                # se risulta una mancanza, la aggiungo alla parte indetraibile
                elif tax_difference < 0:
                    iva_inded = iva_inded + tax_difference
                totale_iva += iva
                invoice_amount_untaxed += base_amount
                totale_iva_inded += iva_inded
                index += 1

            if tax_item:
                if tax_item['tax_code_name'] not in self.localcontext[
                    'tax_codes']:
                    self.localcontext['tax_codes'][tax_item[
                        'tax_code_name']] = {
                        'base': tax_item['base'],
                        'amount': tax_item['amount'],
                        }
                else:
                    self.localcontext['tax_codes'][tax_item[
                        'tax_code_name']]['base'] += tax_item['base']
                    self.localcontext['tax_codes'][tax_item[
                        'tax_code_name']]['amount'] += tax_item['amount']

        self.localcontext['totali'][
            'totale_operazioni'] += invoice_amount_total
        self.localcontext['totali'][
            'totale_imponibili'] += invoice_amount_untaxed
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
