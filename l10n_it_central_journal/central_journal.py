# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2014-2015 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
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

    def _get_move(self, move_ids):
        move_list = self.pool.get(
            'account.move.line').browse(self.cr, self.uid, move_ids)
        return move_list

    def _save_print_info(self, fiscalyear_id, end_date_print,
                         end_row, end_debit, end_credit):
        res = False
        if self.localcontext.get('print_state') == 'def':
            fiscalyear_obj = self.pool.get('account.fiscalyear')
            fiscalyear_ids = fiscalyear_obj.search(
                            self.cr, self.uid, [('id', '=', fiscalyear_id)])
            fiscalyear_data = fiscalyear_obj.browse(
                            self.cr, self.uid, fiscalyear_ids)[0]
            print_info = {
                'date_last_print': end_date_print,
                'progressive_line_number': end_row,
                # 'progressive_page_number': end_page,
                'progressive_debit': end_debit,
                'progressive_credit': end_credit,
            }
            res = fiscalyear_obj.write(
                                self.cr, self.uid, fiscalyear_ids, print_info)
        return res

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_move': self._get_move,
            'save_print_info': self._save_print_info,
        })

    def set_context(self, objects, data, ids, report_type=None):
        self.localcontext.update({
            'l10n_it_count_fiscal_page_base': data['form'].get(
                'fiscal_page_base'),
            'start_row': data['form'].get(
                'start_row'),
            'date_move_line_to': data['form'].get(
                'date_move_line_to'),
            'fiscalyear': data['form'].get(
                'fiscalyear'),
            'print_state': data['form'].get(
                'print_state'),
            'progressive_credit': data['form'].get(
                'progressive_credit'),
            'progressive_debit': data['form'].get(
                'progressive_debit'),
        })
        return super(Parser, self).set_context(
            objects, data, ids, report_type=report_type)


class report_giornale(osv.AbstractModel):
    _name = 'report.l10n_it_central_journal.report_giornale'
    _inherit = 'report.abstract_report'
    _template = 'l10n_it_central_journal.report_giornale'
    _wrapped_report_class = Parser
