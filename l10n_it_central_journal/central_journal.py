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
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
#

from openerp.report import report_sxw
from openerp.osv import osv
import logging

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
