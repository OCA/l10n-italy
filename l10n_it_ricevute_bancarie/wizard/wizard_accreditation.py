# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class RibaAccreditation(models.TransientModel):

    @api.model
    def _get_accreditation_journal_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list('accreditation_journal_id')

    @api.model
    def _get_accreditation_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list('accreditation_account_id')

    @api.model
    def _get_bank_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list('bank_account_id')

    @api.model
    def _get_bank_expense_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list('bank_expense_account_id')

    @api.model
    def _get_accreditation_amount(self):
        if not self.env.context.get('active_id', False):
            return False
        distinta_model = self.env['riba.distinta']
        distinta = distinta_model.browse(self.env.context['active_id'])
        amount = 0.0
        for line in distinta.line_ids:
            amount += line.amount
        return amount

    _name = "riba.accreditation"
    _description = "Bank accreditation"
    accreditation_journal_id = fields.Many2one(
        'account.journal',
        'Accreditation journal',
        domain=[('type', '=', 'bank')],
        default=_get_accreditation_journal_id)
    accreditation_account_id = fields.Many2one(
        'account.account', 'Ri.Ba. bank account',
        default=_get_accreditation_account_id)
    accreditation_amount = fields.Float(
        'Credit amount', default=_get_accreditation_amount)
    bank_account_id = fields.Many2one(
        'account.account',
        'Bank account',
        domain=[('internal_type', '=', 'liquidity')],
        default=_get_bank_account_id)
    bank_amount = fields.Float('Paid amount')
    bank_expense_account_id = fields.Many2one(
        'account.account', 'Bank Expenses account',
        default=_get_bank_expense_account_id)
    expense_amount = fields.Float('Expenses amount')

    def skip(self):
        active_id = self.env.context.get('active_id') or False
        if not active_id:
            raise UserError(_('No active ID found'))
        self.env['riba.distinta'].browse(active_id).signal_workflow(
            'accredited')
        return {'type': 'ir.actions.act_window_close'}

    def create_move(self):
        active_id = self.env.context.get('active_id', False)
        if not active_id:
            raise UserError(_('No active ID found'))
        move_model = self.env['account.move']
        distinta_model = self.env['riba.distinta']
        distinta = distinta_model.browse(active_id)
        wizard = self
        if (
            not wizard.accreditation_journal_id or
            not wizard.accreditation_account_id or
            not wizard.bank_account_id or
            not wizard.bank_expense_account_id
        ):
            raise UserError(_('Every account is mandatory'))
        move_vals = {
            'ref': _('Accreditation Ri.Ba. %s') % distinta.name,
            'journal_id': wizard.accreditation_journal_id.id,
            'line_ids': [
                (0, 0, {
                    'name':  _('Credit'),
                    'account_id': wizard.accreditation_account_id.id,
                    'credit': wizard.accreditation_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name':  _('Bank'),
                    'account_id': wizard.bank_account_id.id,
                    'debit': wizard.bank_amount,
                    'credit': 0.0,
                }),
            ]
        }

        if wizard.expense_amount:
            move_vals['line_ids'].append(
                (0, 0, {
                    'name':  _('Bank'),
                    'account_id': wizard.bank_expense_account_id.id,
                    'debit': wizard.expense_amount,
                    'credit': 0.0,
                }),)

        move = move_model.create(move_vals)
        distinta.write({'accreditation_move_id': move.id})
        distinta_model.browse(active_id).signal_workflow(
            'accredited')
        return {
            'name': _('Accreditation Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id or False,
        }
