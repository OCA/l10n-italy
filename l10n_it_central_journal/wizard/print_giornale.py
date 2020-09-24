# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from datetime import timedelta
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
    _description = "Wizard journal report"

    date_move_line_from = fields.Date(required=True)
    date_move_line_from_view = fields.Date('From date')
    last_def_date_print = fields.Date('Last definitive date print')
    date_move_line_to = fields.Date('To date', required=True)
    daterange = fields.Many2one('date.range',
                                'Date Range',
                                required=True)
    company_id = fields.Many2one(related='daterange.company_id',
                                 readonly=True, store=True)
    progressive_credit = fields.Float('Progressive Credit')
    progressive_debit2 = fields.Float('Progressive Debit')
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
    year_footer = fields.Char(string='Year for Footer',
                              help="Value printed near number "
                                   "of page in the footer")

    @api.onchange('date_move_line_from_view')
    def get_year_footer(self):
        if self.date_move_line_from_view:
            self.year_footer = fields.Date.to_date(
                self.date_move_line_from_view).year

    @api.onchange('daterange')
    def on_change_daterange(self):
        if self.daterange:
            date_start = fields.Date.to_date(self.daterange.date_start)
            date_end = fields.Date.to_date(self.daterange.date_end)

            if self.daterange.date_last_print:
                date_last_print = fields.Date.to_date(
                    self.daterange.date_last_print)
                self.last_def_date_print = date_last_print
                date_start = (date_last_print + timedelta(days=1)).__str__()
            else:
                self.last_def_date_print = None
            self.date_move_line_from = date_start
            self.date_move_line_from_view = date_start
            self.date_move_line_to = date_end
            if self.daterange.progressive_line_number != 0:
                self.start_row = self.daterange.progressive_line_number + 1
            else:
                self.start_row = self.daterange.progressive_line_number
            self.progressive_debit2 = self.daterange.progressive_debit
            self.progressive_credit = self.daterange.progressive_credit

            if self.last_def_date_print == self.daterange.date_end:
                self.date_move_line_from_view = self.last_def_date_print

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
            AND aml.journal_id in %(journal_ids)s
            ORDER BY am.date, am.name
        """
        params = {
            'date_from': wizard.date_move_line_from,
            'date_to': wizard.date_move_line_to,
            'target_type': tuple(target_type),
            'journal_ids': tuple(self.journal_ids.ids)
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
        datas_form['daterange'] = wizard.daterange.id
        return datas_form

    def print_giornale(self):
        wizard = self
        move_line_ids = self.get_line_ids()
        if not move_line_ids:
            raise UserError(_('No documents found in the current selection'))
        datas_form = self._prepare_datas_form()
        datas_form['print_state'] = 'draft'
        datas_form['year_footer'] = wizard.year_footer
        datas = {
            'ids': move_line_ids,
            'model': 'account.move',
            'form': datas_form}
        return self.env.ref(
            'l10n_it_central_journal.action_report_giornale').report_action(
            self, data=datas)

    def print_giornale_final(self):
        wizard = self
        res_company_obj = self.env['res.company']
        if wizard.last_def_date_print and \
                wizard.date_move_line_from <= wizard.last_def_date_print:
            raise UserError(_('Date already printed'))
        else:
            move_line_ids = self.get_line_ids()
            if not move_line_ids:
                raise UserError(
                    _('No documents found in the current selection'))
            datas_form = self._prepare_datas_form()
            datas_form['print_state'] = 'def'
            datas_form['year_footer'] = wizard.year_footer
            datas = {
                'ids': move_line_ids,
                'model': 'account.move',
                'form': datas_form
            }
            company = res_company_obj.search([('id', '=', self.company_id.id)])
            if not company.period_lock_date or company.period_lock_date \
                    < self.date_move_line_to:
                company.sudo().period_lock_date = self.date_move_line_to
            return self.env.ref(
                'l10n_it_central_journal.action_report_giornale').\
                report_action(self, data=datas)
