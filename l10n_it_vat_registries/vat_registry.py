# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014-2015 Agile Business Group sagl
#    (<http://www.agilebg.com>)
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
#

from openerp.report import report_sxw
from openerp.osv import osv
from openerp import _
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):

    def _tax_amounts_by_tax_id(self, move):
        res = {}
        tax_obj = self.pool.get('account.tax')
        for move_line in move.line_id:
            if (
                move_line.tax_code_id and not
                move_line.tax_code_id.exclude_from_registries
            ):
                # eslcudo i conti imposta in base alla natura della
                # stampa e al tipo conto imposta
                if (
                    (
                        self.localcontext['registry_type'] == 'supplier' and
                        move_line.tax_code_id.vat_statement_type == 'credit'
                    ) or
                    ((
                        self.localcontext['registry_type'] == 'customer' or
                        self.localcontext['registry_type'] == 'corrispettivi'
                    ) and
                        move_line.tax_code_id.vat_statement_type == 'debit')
                ):
                    tax = tax_obj.browse(
                        self.cr, self.uid,
                        move_line.tax_code_id.get_tax_by_tax_code())
                    if not res.get(tax.id):
                        res[tax.id] = {'name': tax.name,
                                       'base': 0,
                                       'tax': 0,
                                       }
                        self.localcontext['used_tax_codes'][
                            move_line.tax_code_id.id] = True

                    if move_line.tax_code_id.is_base:
                        # recupero il valore dell'imponibile
                        res[tax.id]['base'] += (
                            move_line.tax_amount *
                            self.localcontext['data']['form']['tax_sign'])
                    else:
                        # recupero il valore dell'imposta
                        res[tax.id]['tax'] += (
                            move_line.tax_amount *
                            self.localcontext['data']['form']['tax_sign'])
        return res

    def _get_move(self, move_ids):
        move_list = self.pool.get(
            'account.move').browse(self.cr, self.uid, move_ids)
        return move_list

    def _get_tax_lines(self, move):
        res = []
        # index è usato per non ripetere la stampa dei dati fattura quando ci
        # sono più codici IVA
        index = 0
        invoice = False
        for move_line in move.line_id:
            if move_line.invoice:
                if invoice and invoice.id != move_line.invoice.id:
                    raise Exception(
                        _("Move %s contains different invoices") % move.name)
                invoice = move_line.invoice
        amounts_by_tax_id = self._tax_amounts_by_tax_id(move)
        for tax_code_id in amounts_by_tax_id:
            tax_item = {
                'tax_code_name': amounts_by_tax_id[tax_code_id]['name'],
                'base': amounts_by_tax_id[tax_code_id]['base'],
                'tax': amounts_by_tax_id[tax_code_id]['tax'],
                'index': index,
                'invoice_date': (invoice and invoice.date_invoice or
                                 move.date or ''),
                'supplier_invoice_number': (
                    invoice and invoice.supplier_invoice_number or '')
            }
            res.append(tax_item)
            index += 1
        return res

    def _get_invoice_total(self, move):
        total = 0.0
        receivable_payable_found = False
        for move_line in move.line_id:
            if move_line.account_id.type == 'receivable':
                total += move_line.debit or (- move_line.credit)
                receivable_payable_found = True
            elif move_line.account_id.type == 'payable':
                total += (- move_line.debit) or move_line.credit
                receivable_payable_found = True
        if receivable_payable_found:
            return abs(total)
        else:
            return abs(move.amount)

    def build_parent_tax_codes(self, tax_code):
        res = {}
        if tax_code.parent_id and tax_code.parent_id.parent_id:
            res[tax_code.parent_id.id] = True
            res.update(self.build_parent_tax_codes(tax_code.parent_id))
        return res

    def is_totally_undeductable(self, tax):
        children_tax_codes = []
        for tax in tax.child_ids:
            children_tax_codes.append(tax.tax_code_id.id)
        if len(set(children_tax_codes)) == 1:
            return True
        else:
            return False

    def get_undeductible_balances(self, tax):
        total_undeduct = 0
        total_deduct = 0
        if self.is_totally_undeductable(tax):
            total_undeduct = self.compute_tax_code_total(
                tax.child_ids[0].tax_code_id)
        else:
            for child in tax.child_ids:
                # deductibile
                if child.tax_code_id and child.account_collected_id:
                    total_deduct = self.compute_tax_code_total(
                        child.tax_code_id)
                # undeductibile
                elif child.tax_code_id:
                    total_undeduct = self.compute_tax_code_total(
                        child.tax_code_id)
        return (total_undeduct, total_deduct)

    def _compute_totals_tax(self, tax_code_ids):
        res = []
        tax_obj = self.pool.get('account.tax')
        tax_code_obj = self.pool.get('account.tax.code')
        tax_codes = tax_code_obj.browse(self.cr, self.uid, tax_code_ids)
        tax_list = []
        for tax_code in tax_codes:
            tax_id = tax_code.get_tax_by_tax_code()
            if tax_id not in tax_list:
                tax_list.append(tax_id)
        tax_list_obj = tax_obj.browse(self.cr, self.uid, tax_list)
        for tax in tax_list_obj:
            total_undeduct = 0
            total_deduct = 0
            total_tax = 0
            total_base = 0
            if tax.nondeductible:
                # detraibile / indetraibile
                # recupero il valore dell'imponibile
                if tax.base_code_id:
                    total_base = self.compute_tax_code_total(tax.base_code_id)
                else:
                    raise Exception(
                        _("Can't compute base amount for tax %s")
                        % tax.name)
                total_undeduct, total_deduct = self.get_undeductible_balances(
                    tax)
                total_tax = total_deduct + total_undeduct
            else:
                # recupero il valore dell'imponibile
                if tax.base_code_id:
                    total_base = self.compute_tax_code_total(tax.base_code_id)
                # recupero il valore dell'imposta
                if tax.tax_code_id:
                    total_tax = self.compute_tax_code_total(tax.tax_code_id)
                total_deduct = total_tax
            res.append((
                tax.name, total_base, total_tax, total_deduct,
                total_undeduct))
        return res

    def compute_tax_code_total(self, tax_code):
        journal_ids = self.localcontext['data']['form']['journal_ids']
        res_dict = {}
        for period_id in self.localcontext['data']['form']['period_ids']:
            # taking the first and only, as tax_code is 1 record
            tax_sum = tax_code.sum_by_period_and_journals(
                period_id, journal_ids)[0]
            if not res_dict.get(tax_code.id):
                res_dict[tax_code.id] = 0.0
            res_dict[tax_code.id] += (
                tax_sum * self.localcontext['data']['form']['tax_sign'])
        return res_dict[tax_code.id]

    def _get_tax_codes(self):
        return self._compute_totals_tax(
            self.localcontext['used_tax_codes'].keys())

    def _get_start_date(self):
        period_obj = self.pool.get('account.period')
        start_date = False
        for period in period_obj.browse(
            self.cr, self.uid,
            self.localcontext['data']['form']['period_ids']
        ):
            period_start = datetime.strptime(period.date_start, '%Y-%m-%d')
            if not start_date or start_date > period_start:
                start_date = period_start
        return start_date.strftime('%Y-%m-%d')

    def _get_end_date(self):
        period_obj = self.pool.get('account.period')
        end_date = False
        for period in period_obj.browse(
            self.cr, self.uid,
            self.localcontext['data']['form']['period_ids']
        ):
            period_end = datetime.strptime(period.date_stop, '%Y-%m-%d')
            if not end_date or end_date < period_end:
                end_date = period_end
        return end_date.strftime('%Y-%m-%d')

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_move': self._get_move,
            'tax_lines': self._get_tax_lines,
            'tax_codes': self._get_tax_codes,
            'used_tax_codes': {},
            'start_date': self._get_start_date,
            'end_date': self._get_end_date,
            'invoice_total': self._get_invoice_total,
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.localcontext.update({
            'registry_type': data['form'].get('registry_type'),
            'only_totals': data['form'].get('only_totals'),
            'tax_registry_name': data['form'].get('tax_registry_name'),
            'l10n_it_count_fiscal_page_base': data['form'].get(
                'fiscal_page_base'),
        })
        return super(Parser, self).set_context(
            objects, data, ids, report_type=report_type)


class ReportRegistroIvaVendite(osv.AbstractModel):
    _name = 'report.l10n_it_vat_registries.report_registro_iva'
    _inherit = 'report.abstract_report'
    _template = 'l10n_it_vat_registries.report_registro_iva'
    _wrapped_report_class = Parser
