# -*- coding: utf-8 -*-
# Author: Gianmarco Conte - Dinamiche Aziendali Srl
# Copyright 2017
# Dinamiche Aziendali Srl <www.dinamicheaziendali.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from datetime import datetime, timedelta
from odoo.tools.misc import flatten


class WizardGiornale(models.TransientModel):
    @api.model
    def _get_journal(self):
        journal_obj = self.env['account.journal']
        journal_ids = journal_obj.search([
            ('central_journal_exclude', '=', False),
        ])
        return journal_ids

    _name = "wizard.giornale"

    date_move_line_from = fields.Date('From date', required=True)
    date_move_line_from_view = fields.Date('From date')
    last_def_date_print = fields.Date('Last definitive date print')
    date_move_line_to = fields.Date('To date', required=True)
    daterange = fields.Many2one('date.range',
                                'Date Range',
                                required=True)
    company_id = fields.Many2one(related='daterange.company_id',
                                 readonly=True, store=True)
    progressive_credit = fields.Float('Progressive Credit')
    progressive_debit2 = fields.Float('Progressive debit')
    print_state = fields.Selection(
        [('print', 'Ready for printing'),
         ('printed', 'Printed')],
        'State',
        default='print',
        readonly=True)
    journal_ids = fields.Many2many(
        'account.journal',
        'giornale_journals_rel',
        'journal_id',
        'giornale_id',
        default=_get_journal,
        string='Journals',
        required=True)
    target_move = fields.Selection([('all', 'All'),
                                    ('posted', 'Posted'),
                                    ('draft', 'Draft')],
                                   'Target Move', default='all')
    fiscal_page_base = fields.Integer('Last printed page', required=True)
    start_row = fields.Integer('Start row', required=True)
    print_row = fields.Integer('Row for page', default=1)
    year_footer = fields.Char(
        string='Year for Footer',
        help="Value printed near number of page in the footer")

    @api.onchange('daterange')
    def on_change_daterange(self):
        if self.daterange:
            self.print_row = self.daterange.print_row
            self.fiscal_page_base = self.daterange.progressive_page_number
            date_start = datetime.strptime(
                self.daterange.date_start, "%Y-%m-%d").date()
            date_end = datetime.strptime(
                self.daterange.date_end, "%Y-%m-%d").date()
            if self.daterange.date_last_print:
                date_last_print = datetime.strptime(
                    self.daterange.date_last_print, "%Y-%m-%d").date()
                self.last_def_date_print = date_last_print
                date_start = (date_last_print + timedelta(days=1)).__str__()
            else:
                self.last_def_date_print = None
            self.date_move_line_from = date_start
            self.date_move_line_from_view = date_start
            self.date_move_line_to = date_end
            if self.daterange.progressive_line_number != 0:
                self.start_row = self.daterange.progressive_line_number
            else:
                self.start_row = self.daterange.progressive_line_number
            self.progressive_debit2 = self.daterange.progressive_debit
            self.progressive_credit = self.daterange.progressive_credit

            if self.last_def_date_print == self.daterange.date_end:
                self.date_move_line_from_view = self.last_def_date_print

    @api.onchange('date_move_line_from')
    def on_change_date_start(self):
        if self.date_move_line_from:
            self.year_footer = str(datetime.strptime(
                self.date_move_line_from, "%Y-%m-%d").year
            )

    def get_line_ids(self):
        wizard = self
        if wizard.target_move == 'all':
            target_type = ['posted', 'draft']
        else:
            target_type = [wizard.target_move]
        sql = """
            SELECT aml.id FROM account_move_line aml
            LEFT JOIN account_move am ON (am.id = aml.move_id)
            WHERE
            aml.date >= %(date_from)s
            AND aml.date <= %(date_to)s
            AND am.state in %(target_type)s
            ORDER BY am.date, am.name
        """
        params = {
            'date_from': wizard.date_move_line_from,
            'date_to': wizard.date_move_line_to,
            'target_type': tuple(target_type)
            }
        self.env.cr.execute(sql, params)
        res = self.env.cr.fetchall()
        move_line_ids = flatten(res)
        return move_line_ids

    def _prepare_datas_form(self):
        wizard = self
        datas_form = {}
        datas_form['date_move_line_from'] = wizard.date_move_line_from
        datas_form['last_def_date_print'] = wizard.last_def_date_print
        datas_form['date_move_line_to'] = wizard.date_move_line_to
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['progressive_debit'] = wizard.progressive_debit2
        datas_form['progressive_credit'] = wizard.progressive_credit
        datas_form['start_row'] = wizard.start_row
        datas_form['print_row'] = wizard.print_row
        datas_form['daterange'] = wizard.daterange.id
        datas_form['year_footer'] = wizard.year_footer
        return datas_form

    def print_giornale(self):

        move_line_ids = self.get_line_ids()
        if not move_line_ids:
            raise UserError(_('No documents found in the current selection'))
        datas_form = self._prepare_datas_form()
        datas_form['print_state'] = 'draft'
        report_name = 'l10n_it_central_journal.report_giornale'
        datas = {
            'ids': move_line_ids,
            'model': 'account.move',
            'form': datas_form}
        return self.env['report'].get_action([], report_name, data=datas)

    def print_giornale_final(self):
        res_company_obj = self.env['res.company']
        # if wizard.date_move_line_from <= wizard.last_def_date_print:
        #     raise UserError(_('Date already printed'))
        # else:
        move_line_ids = self.get_line_ids()
        if not move_line_ids:
            raise UserError(
                _('No documents found in the current selection'))
        datas_form = self._prepare_datas_form()
        datas_form['print_state'] = 'def'
        report_name = 'l10n_it_central_journal.report_giornale'
        datas = {
            'ids': move_line_ids,
            'model': 'account.move',
            'form': datas_form
        }
        company = res_company_obj.search([('id', '=', self.company_id.id)])
        if not company.period_lock_date or company.period_lock_date \
                < self.date_move_line_to:
            company.sudo().period_lock_date = self.date_move_line_to
        return self.env['report'].get_action([], report_name, data=datas)
