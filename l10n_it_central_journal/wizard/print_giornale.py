# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
#    Copyright (C) 2014-2015 Agile Business Group
#    (<http://www.agilebg.com>)
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
#


from odoo import models, fields, api
from odoo.exceptions import Warning as UserError
from datetime import datetime, timedelta
import time


class wizard_giornale(models.TransientModel):
    def _get_fiscalyear(self):
        import pdb;
        pdb.set_trace()
        ctx = dict(self._context or {})
        now = time.strftime('%Y-%m-%d')
        company_id = False
        ids = ctx.get('active_ids', [])
        if ids and context.get('active_model') == 'account.account':
            company_id = self.env['account.account'].browse().company_id.id
        else:
            company_id = self.env['res.users'].browse().company_id.id
        domain = [('company_id', '=', company_id),
                  ('date_start', '<', now),
                  ('date_end', '>', now)]
        fiscalyears = self.env['account.fiscalyear'].search(
            domain, limit=1)
        return fiscalyears and fiscalyears[0] or False

    @api.model
    def _get_journal(self):
        import pdb;
        pdb.set_trace()
        journal_obj = self.env['account.journal']
        journal_ids = journal_obj.search([
            ('central_journal_exclude', '=', False)
            ])
        return journal_ids

    _name = "wizard.giornale"

    date_move_line_from = fields.Date('From date', required=True)
    date_move_line_from_view = fields.Date('From date')
    last_def_date_print = fields.Date('Last definitive date print')
    date_move_line_to = fields.Date('To date', required=True)
    fiscalyear = fields.Many2one('date.range',
                                 'Date Range',
                                 required=True)
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

    @api.onchange('fiscalyear')
    def on_change_fiscalyear(self):
        import pdb;
        pdb.set_trace()
        if self.fiscalyear:
            date_start = datetime.strptime(
                self.fiscalyear.date_start, "%Y-%m-%d").date()
            date_end = datetime.strptime(
                self.fiscalyear.date_end, "%Y-%m-%d").date()
            if self.fiscalyear.date_last_print:
                date_last_print = datetime.strptime(
                    self.fiscalyear.date_last_print, "%Y-%m-%d").date()
                self.last_def_date_print = date_last_print
                date_start = (date_last_print + timedelta(days=1)).__str__()
            else:
                self.last_def_date_print = None

            self.date_move_line_from = date_start
            self.date_move_line_from_view = date_start
            self.date_move_line_to = date_end
            self.start_row = self.fiscalyear.progressive_line_number+1
            self.progressive_debit2 = self.fiscalyear.progressive_debit
            self.progressive_credit = self.fiscalyear.progressive_credit

    @api.multi
    @api.model
    def print_giornale(self):
        # import pdb; pdb.set_trace()
        # wizard = self.browse()
        wizard = self
        # wizard = self.browse(self._context)
        # wizard = self.browse(cr, uid, ids[0], context=context)

        if wizard.target_move == 'all':
            target_type = ['posted', 'draft']
        else:
            target_type = [wizard.target_move]

        #controllare move_line_obj che penso deve essere una lista
        move_line_obj = self.env['account.move.line']
        move_line_ids = move_line_obj.search([
            ('date', '>=', wizard.date_move_line_from),
            ('date', '<=', wizard.date_move_line_to),
            ('move_id.state', 'in', target_type)
            ], order='date, move_id asc')
        if not move_line_ids:
            raise UserError(('No documents found in the current selection'))
        datas = {}
        datas_form = {}
        datas_form['date_move_line_from'] = wizard.date_move_line_from
        datas_form['last_def_date_print'] = wizard.last_def_date_print
        datas_form['date_move_line_to'] = wizard.date_move_line_to
        datas_form['fiscal_page_base'] = wizard.fiscal_page_base
        datas_form['progressive_debit'] = wizard.progressive_debit2
        datas_form['progressive_credit'] = wizard.progressive_credit
        datas_form['start_row'] = wizard.start_row
        datas_form['fiscalyear'] = wizard.fiscalyear.id
        datas_form['print_state'] = 'draft'
        report_name = 'l10n_it_central_journal.report_giornale'
        datas = {
            'ids': move_line_ids.ids,
            # 'ids': move_line_ids,
            'model': 'account.move',
            'form': datas_form
        }
        import pdb;
        pdb.set_trace()
        # return self.env['report'].get_action([], report_name)
        return self.env['report'].get_action([], report_name, data=datas)

    def print_giornale_final(self):
        wizard = self
        if wizard.date_move_line_from <= wizard.last_def_date_print:
            raise UserError(('Date already printed'))
        else:
            if wizard.target_move == 'all':
                target_type = ['posted', 'draft']
            else:
                target_type = [wizard.target_move]

            move_line_obj = self.env['account.move.line']
            move_line_ids = move_line_obj.search([
                ('date', '>=', wizard.date_move_line_from),
                ('date', '<=', wizard.date_move_line_to),
                ('move_id.state', 'in', target_type)
                ], order='date, move_id asc')
            if not move_line_ids:
                raise UserError(
                    ('No documents found in the current selection'))
            datas = {}
            datas_form = {}
            datas_form['date_move_line_from'] = wizard.date_move_line_from
            datas_form['last_def_date_print'] = wizard.last_def_date_print
            datas_form['date_move_line_to'] = wizard.date_move_line_to
            datas_form['fiscal_page_base'] = wizard.fiscal_page_base
            datas_form['progressive_debit'] = wizard.progressive_debit2
            datas_form['progressive_credit'] = wizard.progressive_credit
            datas_form['fiscalyear'] = wizard.fiscalyear.id
            datas_form['start_row'] = wizard.start_row
            datas_form['print_state'] = 'def'
            report_name = 'l10n_it_central_journal.report_giornale'
            datas = {
                'ids': move_line_ids,
                'model': 'account.move',
                'form': datas_form
            }
            return self.env['report'].get_action([], report_name, data=datas)
