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


class riba_accreditation(orm.TransientModel):

    def _get_accreditation_journal_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta(
            cr, uid, 'accreditation_journal_id', context=context)

    def _get_accreditation_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta(
            cr, uid, 'accreditation_account_id', context=context)

    def _get_bank_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta(
            cr, uid, 'bank_account_id', context=context)

    def _get_bank_expense_account_id(self, cr, uid, context=None):
        return self.pool.get(
            'riba.configurazione'
        ).get_default_value_by_distinta(
            cr, uid, 'bank_expense_account_id', context=context)

    def _get_accreditation_amount(self, cr, uid, context=None):
        if context is None:
            context = {}
        if not context.get('active_id', False):
            return False
        distinta_pool = self.pool.get('riba.distinta')
        distinta = distinta_pool.browse(
            cr, uid, context['active_id'], context=context)
        amount = 0.0
        for line in distinta.line_ids:
            amount += line.amount
        return amount

    _name = "riba.accreditation"
    _description = "Bank accreditation"
    _columns = {
        'accreditation_journal_id': fields.many2one(
            'account.journal', "Accreditation journal",
            domain=[('type', '=', 'bank')]),
        'accreditation_account_id': fields.many2one(
            'account.account', "Ri.Ba. bank account"),
        'accreditation_amount': fields.float('Credit amount'),
        'bank_account_id': fields.many2one('account.account', "Bank account",
                                           domain=[(
                                               'type', '=', 'liquidity')]),
        'bank_amount': fields.float('Versed amount'),
        'bank_expense_account_id': fields.many2one(
            'account.account', "Bank Expenses account"),
        'expense_amount': fields.float('Expenses amount'),
    }

    _defaults = {
        'accreditation_journal_id': _get_accreditation_journal_id,
        'accreditation_account_id': _get_accreditation_account_id,
        'bank_account_id': _get_bank_account_id,
        'bank_expense_account_id': _get_bank_expense_account_id,
        'accreditation_amount': _get_accreditation_amount,
    }

    def skip(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wf_service = netsvc.LocalService("workflow")
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            raise orm.except_orm(_('Error'), _('No active ID found'))
        wf_service.trg_validate(
            uid, 'riba.distinta', active_id, 'accredited', cr)
        return {'type': 'ir.actions.act_window_close'}

    def create_move(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wf_service = netsvc.LocalService("workflow")
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            raise orm.except_orm(_('Error'), _('No active ID found'))
        move_pool = self.pool.get('account.move')
        distinta_pool = self.pool.get('riba.distinta')
        distinta = distinta_pool.browse(cr, uid, active_id, context=context)
        wizard = self.browse(cr, uid, ids)[0]
        if (
            not wizard.accreditation_journal_id or
            not wizard.accreditation_account_id or
            not wizard.bank_account_id or
            not wizard.bank_expense_account_id
        ):
            raise orm.except_orm(_('Error'), _('Every account is mandatory'))
        move_vals = {
            'ref': _('Accreditation Ri.Ba. %s') % distinta.name,
            'journal_id': wizard.accreditation_journal_id.id,
            'line_id': [
                (0, 0, {
                    'name': _('Credit'),
                    'account_id': wizard.accreditation_account_id.id,
                    'credit': wizard.accreditation_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name': _('Bank'),
                    'account_id': wizard.bank_account_id.id,
                    'debit': wizard.bank_amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name': _('Bank'),
                    'account_id': wizard.bank_expense_account_id.id,
                    'debit': wizard.expense_amount,
                    'credit': 0.0,
                }),
            ]
        }
        move_id = move_pool.create(cr, uid, move_vals, context=context)
        distinta.write({'accreditation_move_id': move_id})
        wf_service.trg_validate(
            uid, 'riba.distinta', active_id, 'accredited', cr)
        return {
            'name': _('Accreditation Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move_id or False,
        }
