# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from openerp.tools import float_is_zero


class AccountFiscalyearClosingMapping(models.Model):
    _name = "account.fiscalyear.closing.mapping"
    _description = "Fiscal year closing move account mapping"

    name = fields.Char(string="Description")
    fyc_config_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.config', index=True,
        string="Fiscal year closing config", readonly=True, required=True,
        ondelete='cascade')
    src_account_ids = fields.Many2many(
        comodel_name='account.account', string="Source accounts",
        required=True)
    dst_account_id = fields.Many2one(
        comodel_name='account.account', string="Destination account")

    @api.multi
    def dst_move_line_prepare(self, dst_id, balance, partner_id=False):
        self.ensure_one()
        move_line = {}
        precision = self.env['decimal.precision'].precision_get('Account')
        journal_id = self.fyc_config_id.journal_id.id
        fyc_id = self.fyc_config_id.fyc_id.id
        date = self.fyc_config_id.fyc_id.date_end
        if self.fyc_config_id.move_type == 'opening':
            date = self.fyc_config_id.fyc_id.date_opening
        if not float_is_zero(balance, precision_digits=precision):
            move_line = {
                'account_id': dst_id,
                'debit': balance < 0 and -balance,
                'credit': balance > 0 and balance,
                'name': _('Result'),
                'date': date,
                'fyc_id': fyc_id,
                'partner_id': partner_id,
                'journal_id': journal_id,
            }
        return move_line

    @api.multi
    def move_line_prepare(self, account, account_lines, partner_id=False):
        self.ensure_one()
        move_line = {}
        balance = 0
        precision = self.env['decimal.precision'].precision_get('Account')
        description = self.name
        journal_id = self.fyc_config_id.journal_id.id
        fyc_id = self.fyc_config_id.fyc_id.id
        date = self.fyc_config_id.fyc_id.date_end
        if self.fyc_config_id.move_type == 'opening':
            date = self.fyc_config_id.fyc_id.date_opening
        if account_lines:
            balance = (
                sum(account_lines.mapped('debit')) -
                sum(account_lines.mapped('credit')))
            if not float_is_zero(balance, precision_digits=precision):
                move_line = {
                    'account_id': account.id,
                    'debit': balance < 0 and -balance,
                    'credit': balance > 0 and balance,
                    'name': description,
                    'date': date,
                    'fyc_id': fyc_id,
                    'partner_id': partner_id,
                    'journal_id': journal_id,
                }
            else:
                balance = 0
        return balance, move_line

    @api.multi
    def account_lines_get(self, account):
        self.ensure_one()
        start = self.fyc_config_id.fyc_id.date_start
        end = self.fyc_config_id.fyc_id.date_end
        company_id = self.fyc_config_id.fyc_id.company_id.id
        return self.env['account.move.line'].search([
            ('company_id', '=', company_id),
            ('account_id', '=', account.id),
            ('date', '>=', start),
            ('date', '<=', end),
        ])

    @api.multi
    def move_line_partner_prepare(self, account, partner):
        self.ensure_one()
        move_line = {}
        balance = partner.get('debit', 0.) - partner.get('credit', 0.)
        precision = self.env['decimal.precision'].precision_get('Account')
        description = self.name
        partner_id = partner.get('partner_id')
        if partner_id:
            partner_id = partner_id[0]
        journal_id = self.fyc_config_id.journal_id.id
        fyc_id = self.fyc_config_id.fyc_id.id
        date = self.fyc_config_id.fyc_id.date_end
        if self.fyc_config_id.move_type == 'opening':
            date = self.fyc_config_id.fyc_id.date_opening
        if not float_is_zero(balance, precision_digits=precision):
            move_line = {
                'account_id': account.id,
                'debit': balance < 0 and -balance,
                'credit': balance > 0 and balance,
                'name': description,
                'date': date,
                'fyc_id': fyc_id,
                'partner_id': partner_id,
                'journal_id': journal_id,
            }
        else:
            balance = 0
        return balance, move_line

    @api.multi
    def account_partners_get(self, account):
        self.ensure_one()
        start = self.fyc_config_id.fyc_id.date_start
        end = self.fyc_config_id.fyc_id.date_end
        company_id = self.fyc_config_id.fyc_id.company_id.id
        return self.env['account.move.line'].read_group([
            ('company_id', '=', company_id),
            ('account_id', '=', account.id),
            ('date', '>=', start),
            ('date', '<=', end),
        ], ['partner_id', 'credit', 'debit'], ['partner_id'])
