# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014 Agile Business Group sagl
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

    def _tax_amounts_by_code(self, move):
        res = {}
        for move_line in move.line_id:
            if (
                move_line.tax_code_id
                and not move_line.tax_code_id.exclude_from_registries
                and move_line.tax_amount
            ):
                if not res.get(move_line.tax_code_id.id):
                    res[move_line.tax_code_id.id] = 0.0
                    self.localcontext['used_tax_codes'][
                        move_line.tax_code_id.id] = True
                res[move_line.tax_code_id.id] += (
                    move_line.tax_amount
                    * self.localcontext['data']['form']['tax_sign'])
        return res

    def _get_move(self, move_ids):
        move_list = self.pool.get(
            'account.move').browse(self.cr, self.uid, move_ids)
        return move_list

    def _get_tax_lines(self, move):
        res = []
        tax_code_obj = self.pool.get('account.tax.code')
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
        amounts_by_code = self._tax_amounts_by_code(move)
        for tax_code_id in amounts_by_code:
            tax_code = tax_code_obj.browse(self.cr, self.uid, tax_code_id)
            tax_item = {
                'tax_code_name': tax_code.name,
                'amount': amounts_by_code[tax_code_id],
                'index': index,
                'invoice_date': (invoice and invoice.date_invoice
                                 or move.date or ''),
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

    def _compute_totals(self, tax_code_ids):
        res = []
        res_dict = {}
        tax_code_obj = self.pool.get('account.tax.code')
        for period_id in self.localcontext['data']['form']['period_ids']:
            for tax_code in tax_code_obj.browse(
                self.cr, self.uid,
                tax_code_ids, context={
                    'period_id': period_id,
                }
            ):
                if not res_dict.get(tax_code.id):
                    res_dict[tax_code.id] = 0.0
                res_dict[tax_code.id] += (
                    tax_code.sum_period
                    * self.localcontext['data']['form']['tax_sign'])
        for tax_code_id in res_dict:
            tax_code = tax_code_obj.browse(self.cr, self.uid, tax_code_id)
            if res_dict[tax_code_id]:
                res.append(
                    (tax_code.name, res_dict[tax_code_id], tax_code.is_base))
        return res

    def _get_tax_codes(self):
        return self._compute_totals(self.localcontext['used_tax_codes'].keys())

    def _get_tax_codes_totals(self):
        parent_codes = {}
        tax_code_obj = self.pool.get('account.tax.code')
        for tax_code in tax_code_obj.browse(
            self.cr, self.uid,
            self.localcontext['used_tax_codes'].keys()
        ):
            parent_codes.update(self.build_parent_tax_codes(tax_code))
        return self._compute_totals(parent_codes.keys())

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
            'tax_codes_totals': self._get_tax_codes_totals,
            'used_tax_codes': {},
            'start_date': self._get_start_date,
            'end_date': self._get_end_date,
            'invoice_total': self._get_invoice_total,
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.localcontext.update({
            'registry_type': data['form'].get('registry_type'),
        })
        return super(Parser, self).set_context(
            objects, data, ids, report_type=report_type)


class report_registro_iva_vendite(osv.AbstractModel):
    _name = 'report.l10n_it_vat_registries.report_registro_iva'
    _inherit = 'report.abstract_report'
    _template = 'l10n_it_vat_registries.report_registro_iva'
    _wrapped_report_class = Parser
