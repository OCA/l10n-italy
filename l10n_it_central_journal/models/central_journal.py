# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import models, api
from odoo.tools.misc import formatLang
import logging

_logger = logging.getLogger(__name__)


class ReportGiornale(models.AbstractModel):
    _name = 'report.l10n_it_central_journal.report_giornale'
    _description = "Journal report"

    @api.model
    def _get_report_values(self, docids, data=None):
        lang_code = self._context.get('company_id',
                                      self.env.user.company_id.partner_id.lang)
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        return {
            'doc_ids': data['ids'],
            'doc_model': self.env['account.move.line'],
            'data': data,
            'docs': self.env['account.move.line'].browse(data['ids']),
            'get_move': self._get_move,
            'save_print_info': self._save_print_info,
            'env': self.env,
            'formatLang': formatLang,
            'l10n_it_count_fiscal_page_base': data['form']['fiscal_page_base'],
            'start_row': data['form']['start_row'],
            'date_move_line_to': data['form']['date_move_line_to'],
            'daterange': data['form']['daterange'],
            'print_state': data['form']['print_state'],
            'year_footer': data['form']['year_footer'],
            'progressive_credit': data['form']['progressive_credit'],
            'progressive_debit': data['form']['progressive_debit'],
            'date_format': date_format,
        }

    def _get_move(self, move_ids):
        move_list = self.env[
            'account.move.line'].browse(move_ids)
        return move_list

    def _save_print_info(self, daterange_id, print_state, end_date_print,
                         end_row, end_debit, end_credit):
        res = False
        if print_state == 'def':
            datarange_obj = self.env['date.range']
            daterange_ids = datarange_obj.search([('id', '=', daterange_id)])
            print_info = {
                'date_last_print': end_date_print,
                'progressive_line_number': end_row,
                'progressive_debit': end_debit,
                'progressive_credit': end_credit,
            }
            res = daterange_ids.write(print_info)
        return res
