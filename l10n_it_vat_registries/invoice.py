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

    def _tax_amounts_by_code(self, move):
        res={}
        for move_line in move.line_id:
            if move_line.tax_code_id and move_line.tax_amount:
                if not res.get(move_line.tax_code_id.id):
                    res[move_line.tax_code_id.id] = 0.0
                    self.localcontext['used_tax_codes'][move_line.tax_code_id.id] = True
                res[move_line.tax_code_id.id] += move_line.tax_amount
        return res

    def _get_tax_lines(self, move):
        res=[]
        tax_code_obj=self.pool.get('account.tax.code')
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        invoice = False
        for move_line in move.line_id:
            if move_line.invoice:
                if invoice and invoice.id != move_line.invoice.id:
                    raise Exception(_("Move %s contains different invoices") % move.name)
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
                }
            res.append(tax_item)
            index += 1

        return res
    
    def _get_tax_codes(self):
        res=[]
        tax_code_obj = self.pool.get('account.tax.code')
        for tax_code in tax_code_obj.browse(self.cr, self.uid,
            self.localcontext['used_tax_codes'].keys(), context={
            'period_id': self.localcontext['period_id'],
            }):
            if tax_code.sum_period:
                res.append((tax_code.name,tax_code.sum_period))
        return res

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'tax_lines': self._get_tax_lines,
            'tax_codes': self._get_tax_codes,
            'used_tax_codes': {},
            'period_id': context.get('period_id')
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
