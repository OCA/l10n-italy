# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
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
#

from openerp.osv import fields, orm
from tools.translate import _
import netsvc


class riba_unsolved(orm.TransientModel):

    def _get_unsolved_journal_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'unsolved_journal_id', context=context)

    def _get_effects_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'acceptance_account_id', context=context)

    def _get_effects_amount(self, cr, uid, context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        return self.pool.get(
            'riba.distinta.line'
        ).browse(cr, uid, context['active_id'], context=context).amount

    def _get_riba_bank_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'accreditation_account_id', context=context)

    def _get_overdue_effects_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'overdue_effects_account_id', context=context)

    def _get_bank_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'bank_account_id', context=context)

    def _get_bank_expense_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta_line(
            cr, uid, 'protest_charge_account_id', context=context)

    _name = "riba.unsolved"
    _columns = {
        'unsolved_journal_id': fields.many2one(
            'account.journal', "Unsolved journal",
            domain=[('type', '=', 'bank')]),
        'effects_account_id': fields.many2one(
            'account.account', "Effects account",
            domain=[('type', '=', 'receivable')]),
        'effects_amount': fields.float('Effects amount'),
        'riba_bank_account_id': fields.many2one(
            'account.account', "Ri.Ba. bank account"),
        'riba_bank_amount': fields.float('Ri.Ba. bank amount'),
        'overdue_effects_account_id': fields.many2one(
            'account.account', "Overdue Effects account",
            domain=[('type', '=', 'receivable')]),
        'overdue_effects_amount': fields.float('Overdue Effects amount'),
        'bank_account_id': fields.many2one('account.account', "Bank account",
                                           domain=[(
                                               'type', '=', 'liquidity')]),
        'bank_amount': fields.float('Taken amount'),
        'bank_expense_account_id': fields.many2one(
            'account.account', "Bank Expenses account"),
        'expense_amount': fields.float('Expenses amount'),
    }

    _defaults = {
        'unsolved_journal_id': _get_unsolved_journal_id,
        'effects_account_id': _get_effects_account_id,
        'effects_amount': _get_effects_amount,
        'riba_bank_account_id': _get_riba_bank_account_id,
        'riba_bank_amount': _get_effects_amount,
        'overdue_effects_account_id': _get_overdue_effects_account_id,
        'overdue_effects_amount': _get_effects_amount,
        'bank_account_id': _get_bank_account_id,
        'bank_expense_account_id': _get_bank_expense_account_id,
    }

    def skip(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wf_service = netsvc.LocalService("workflow")
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            raise orm.except_orm(_('Error'), _('No active ID found'))
        line_pool = self.pool.get('riba.distinta.line')
        line_pool.write(cr, uid, active_id,
                        {'state': 'unsolved'}, context=context)
        wf_service.trg_validate(
            uid, 'riba.distinta', line_pool.browse(
                cr, uid, active_id).distinta_id.id, 'unsolved', cr)
        return {'type': 'ir.actions.act_window_close'}

    def create_move(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wf_service = netsvc.LocalService("workflow")
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            raise orm.except_orm(_('Error'), _('No active ID found'))
        move_pool = self.pool.get('account.move')
        invoice_pool = self.pool.get('account.invoice')
        move_line_pool = self.pool.get('account.move.line')
        distinta_line = self.pool.get('riba.distinta.line').browse(
            cr, uid, active_id, context=context)
        wizard = self.browse(cr, uid, ids)[0]
        if (
            not wizard.unsolved_journal_id or
            not wizard.effects_account_id or
            not wizard.riba_bank_account_id or
            not wizard.overdue_effects_account_id or
            not wizard.bank_account_id or
            not wizard.bank_expense_account_id
        ):
            raise orm.except_orm(_('Error'), _('Every account is mandatory'))
        move_vals = {
            'ref': _('Unsolved Ri.Ba. %s - line %s') % (
                distinta_line.distinta_id.name, distinta_line.sequence),
            'journal_id': wizard.unsolved_journal_id.id,
            'line_id': [
                (0, 0, {
                    'name': _('Effects'),
                    'account_id': wizard.effects_account_id.id,
                    'partner_id': distinta_line.partner_id.id,
                    'credit': wizard.effects_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name': _('Ri.Ba. Bank'),
                    'account_id': wizard.riba_bank_account_id.id,
                    'debit': wizard.riba_bank_amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': _('Overdue Effects'),
                    'account_id': wizard.overdue_effects_account_id.id,
                    'debit': wizard.overdue_effects_amount,
                    'credit': 0.0,
                    'partner_id': distinta_line.partner_id.id,
                    'date_maturity': distinta_line.due_date,
                }),
                (0, 0, {
                    'name': _('Bank'),
                    'account_id': wizard.bank_account_id.id,
                    'credit': wizard.bank_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name': _('Expenses'),
                    'account_id': wizard.bank_expense_account_id.id,
                    'debit': wizard.expense_amount,
                    'credit': 0.0,
                }),
            ]
        }
        move_id = move_pool.create(cr, uid, move_vals, context=context)

        to_be_reconciled = []
        for move_line in move_pool.browse(
            cr, uid, move_id, context=context
        ).line_id:
            if move_line.account_id.id == wizard.overdue_effects_account_id.id:
                for riba_move_line in distinta_line.move_line_ids:
                    invoice_ids = []
                    if riba_move_line.move_line_id.invoice:
                        invoice_ids = [riba_move_line.move_line_id.invoice.id]
                    elif riba_move_line.move_line_id.unsolved_invoice_ids:
                        invoice_ids = [
                            i.id for i in
                            riba_move_line.move_line_id.unsolved_invoice_ids
                        ]
                    invoice_pool.write(cr, uid, invoice_ids, {
                        'unsolved_move_line_ids': [(4, move_line.id)],
                    }, context=context)
            if move_line.account_id.id == wizard.effects_account_id.id:
                to_be_reconciled.append(move_line.id)
        for acceptance_move_line in distinta_line.acceptance_move_id.line_id:
            if (
                acceptance_move_line.account_id.id ==
                wizard.effects_account_id.id
            ):
                to_be_reconciled.append(acceptance_move_line.id)

        distinta_line.write({
            'unsolved_move_id': move_id,
            'state': 'unsolved',
        })
        move_line_pool.reconcile_partial(
            cr, uid, to_be_reconciled, context=context)
        wf_service.trg_validate(
            uid, 'riba.distinta', distinta_line.distinta_id.id, 'unsolved', cr)
        return {
            'name': _('Unsolved Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move_id or False,
        }
