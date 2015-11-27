# -*- encoding: utf-8 -*-
#
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2015 Link It Spa
#    (<http://www.linkgroup.it/>)
#    Copyright (C) 2014-2015 Agile Business Group
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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#


from openerp import models, fields, api, _
from openerp.exceptions import Warning
from datetime import datetime, date, timedelta
import openerp.addons.decimal_precision as dp


class wizard_giornale(models.TransientModel):
    def _get_fiscalyear(self, cr, uid, context=None):
        ctx = dict(self._context or {})
        now = time.strftime('%Y-%m-%d')
        company_id = False
        ids = ctx.get('active_ids', [])
        if ids and context.get('active_model') == 'account.account':
            company_id = self.pool.get('account.account').browse(
                                cr, uid, ids[0], context=context).company_id.id
        else:
            company_id = self.pool.get('res.users').browse(
                                    cr, uid, uid, context=ctx).company_id.id
        domain = [('company_id', '=', company_id),
                  ('date_start', '<', now),
                  ('date_stop', '>', now)]
        fiscalyears = self.pool.get('account.fiscalyear').search(
                                                            domain, limit=1)
        return fiscalyears and fiscalyears[0] or False

    @api.model
    def _get_journal(self):
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
    fiscalyear = fields.Many2one('account.fiscalyear',
                                 'Fiscal Year',
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
        if self.fiscalyear:
            date_start = datetime.strptime(
                                self.fiscalyear.date_start, "%Y-%m-%d").date()
            date_stop = datetime.strptime(
                                self.fiscalyear.date_stop, "%Y-%m-%d").date()
            if self.fiscalyear.date_last_print:
                date_last_print = datetime.strptime(
                            self.fiscalyear.date_last_print, "%Y-%m-%d").date()
                self.last_def_date_print = date_last_print
                date_start = (date_last_print + timedelta(days=1)).__str__()
            else:
                self.last_def_date_print = None

            self.date_move_line_from = date_start
            self.date_move_line_from_view = date_start
            self.date_move_line_to = date_stop
            self.start_row = self.fiscalyear.progressive_line_number+1
            self.progressive_debit2 = self.fiscalyear.progressive_debit
            self.progressive_credit = self.fiscalyear.progressive_credit

    def print_giornale(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)

        if wizard.target_move == 'all':
            target_type = ['posted', 'draft']
        else:
            target_type = [wizard.target_move]

        move_line_obj = self.pool['account.move.line']
        move_line_ids = move_line_obj.search(cr, uid, [
            ('date', '>=', wizard.date_move_line_from),
            ('date', '<=', wizard.date_move_line_to),
            ('move_id.state', 'in', target_type)
            ], order='date, move_id asc')
        if not move_line_ids:
            raise Warning(_('No documents found in the current selection'))
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
            'ids': move_line_ids,
            'model': 'account.move',
            'form': datas_form
        }
        return self.pool['report'].get_action(
            cr, uid, [], report_name, data=datas, context=context)

    def print_giornale_final(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        if wizard.date_move_line_from <= wizard.last_def_date_print:
            raise Warning(_('data già stampata'))
            return False
        else:
            if wizard.target_move == 'all':
                target_type = ['posted', 'draft']
            else:
                target_type = [wizard.target_move]

            move_line_obj = self.pool['account.move.line']
            move_line_ids = move_line_obj.search(cr, uid, [
                ('date', '>=', wizard.date_move_line_from),
                ('date', '<=', wizard.date_move_line_to),
                ('move_id.state', 'in', target_type)
                ], order='date, move_id asc')
            if not move_line_ids:
                raise Warning(_('No documents found in the current selection'))
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
            return self.pool['report'].get_action(
                cr, uid, [], report_name, data=datas, context=context)
