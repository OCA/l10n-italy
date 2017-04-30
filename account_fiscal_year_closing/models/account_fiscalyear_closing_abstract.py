# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountFiscalyearClosingAbstract(models.AbstractModel):
    _name = "account.fiscalyear.closing.abstract"

    name = fields.Char(string="Description", required=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string="Company", ondelete='cascade',
    )
    check_draft_moves = fields.Boolean(
        string="Check draft moves", default=True,
        help="Checks that there are no draft moves on the fiscal year "
             "that is being closed. Non-confirmed moves won't be taken in "
             "account on the closing operations.",
    )


class AccountFiscalyearClosingConfigAbstract(models.AbstractModel):
    _name = "account.fiscalyear.closing.config.abstract"
    _order = "sequence asc, id asc"

    name = fields.Char(string="Description", required=True)
    sequence = fields.Integer(string="Sequence", index=True, default=1)
    code = fields.Char(string="Unique code", required=True)
    inverse = fields.Char(
        string="Inverse config",
        help="Configuration code to inverse its move",
    )
    reconcile = fields.Boolean(
        string="Reconcile", help="Reconcile inverse move",
    )
    move_type = fields.Selection(
        selection=[
            ('closing', 'Closing'),
            ('opening', 'Opening'),
            ('loss_profit', 'Loss & Profit'),
            ('other', 'Other'),
        ], string="Move type", default='closing',
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal", string="Journal",
    )
    closing_type_default = fields.Selection(
        selection=[
            ('balance', 'Balance'),
            ('unreconciled', 'Un-reconciled'),
        ], string="Default closing type", required=True, default='balance',
    )


class AccountFiscalyearClosingMappingAbstract(models.AbstractModel):
    _name = "account.fiscalyear.closing.mapping.abstract"

    name = fields.Char(string="Description")


class AccountFiscalyearClosingTypeAbstract(models.AbstractModel):
    _name = "account.fiscalyear.closing.type.abstract"

    closing_type = fields.Selection(
        selection=[
            ('balance', 'Balance'),
            ('unreconciled', 'Un-reconciled'),
        ], string="Default closing type", required=True,
        default='unreconciled',
    )
    account_type_id = fields.Many2one(
        comodel_name='account.account.type', string="Account type",
        required=True,
    )
