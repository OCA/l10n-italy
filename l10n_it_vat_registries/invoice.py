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
                res[move_line.tax_code_id.id] += move_line.tax_amount
        return res

    def _get_tax_lines(self, move):
        res=[]
        tax_code_obj=self.pool.get('account.tax.code')
        # index è usato per non ripetere la stampa dei dati fattura quando ci sono più codici IVA
        index=0
        for tax_code_id in self._tax_amounts_by_code(move):
            tax_code = tax_code_obj.browse(cr, uid, tax_code_id, context)
            tax_item = {
                'tax_code_name': move_line.tax_code_id.name,
                'amount': actual_tax_amount,
                'index': index,
                'amount_total': invoice_amount_total, #TODO print curr
                }
            res.append(tax_item)
            index += 1

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
