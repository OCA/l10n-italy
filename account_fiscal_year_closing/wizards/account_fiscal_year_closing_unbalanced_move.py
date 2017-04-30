# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountFiscalYearClosingUnbalancedMove(models.TransientModel):
    _name = 'account.fiscalyear.closing.unbalanced.move'

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        readonly=True,
    )
    ref = fields.Char(
        string="Reference",
        readonly=True,
    )
    date = fields.Date(
        string="Date",
        readonly=True,
    )
    line_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.unbalanced.move.line',
        inverse_name='move_id',
        string="Unbalanced move lines",
        readonly=True,
    )


class AccountFiscalYearClosingUnbalancedMoveLine(models.TransientModel):
    _name = 'account.fiscalyear.closing.unbalanced.move.line'

    move_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.unbalanced.move',
        string="Unbalanced move",
    )
    account_id = fields.Many2one(
        comodel_name='account.account',
        string="Account",
    )
    credit = fields.Float()
    debit = fields.Float()
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
    )
    name = fields.Char()
