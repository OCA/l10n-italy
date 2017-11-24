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

# from openerp.report import report_sxw
from odoo.report import report_sxw
from odoo import models, fields, api
import logging


_logger = logging.getLogger(__name__)


class Parser(report_sxw.rml_parse):

    def _get_move(self, move_ids):
        import pdb;
        pdb.set_trace()
        move_list = self.env[
            'account.move.line'].browse(move_ids)
        # move_list = self.pool.get(
        #     'account.move.line').browse(self.cr, self.uid, move_ids)
        return move_list

    def _save_print_info(self, fiscalyear_id, end_date_print,
                         end_row, end_debit, end_credit):
        import pdb; pdb.set_trace()
        res = False
        if self.localcontext.get('print_state') == 'def':
            datarange_obj = self.env['date.range']
            # fiscalyear_obj = self.pool.get('account.fiscalyear')
            fiscalyear_ids = datarange_obj.search(
                self.cr, self.uid, [('id', '=', fiscalyear_id)])
            print_info = {
                'date_last_print': end_date_print,
                'progressive_line_number': end_row,
                'progressive_debit': end_debit,
                'progressive_credit': end_credit,
            }
            res = datarange_obj.write(
                self.cr, self.uid, fiscalyear_ids, print_info)
        return res

    # def __init__(self, cr, uid, name, context):
    #     super(Parser, self).__init__(cr, uid, name, context=context)
    # def __init__(self, name):
    #     import pdb; pdb.set_trace()
    #     super(Parser, self).__init__(name)
    #     self.localcontext.update({
    #         'get_move': self._get_move,
    #         'save_print_info': self._save_print_info,
    #     })
    #     import pdb; pdb.set_trace()

    def __init__(self, context):
        super(Parser, self).__init__(context=context)
        self.localcontext.update({
            'get_move': self._get_move,
            'save_print_info': self._save_print_info,
        })

    # def set_context(self, objects, data, report_type=None):
    def set_context(self, objects, data):
        import pdb;
        pdb.set_trace()
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
        # import pdb;
        # pdb.set_trace()
        return super(Parser, self).set_context(
            objects, data, report_type=report_type)





class report_giornale(models.AbstractModel):
    _name = 'report.l10n_it_central_journal.report_giornale'
    _inherit = 'report.abstract_report'
    _template = 'l10n_it_central_journal.report_giornale'
    _wrapped_report_class = Parser
