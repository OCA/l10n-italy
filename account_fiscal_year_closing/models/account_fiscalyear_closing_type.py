# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountFiscalyearClosingType(models.Model):
    _name = "account.fiscalyear.closing.type"
    _description = "Fiscal year closing type"

    fyc_config_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing.config', index=True,
        string="Fiscal year closing config", readonly=True, required=True,
        ondelete='cascade')
    closing_type = fields.Selection(selection=[
        ('balance', 'Balance'),
        ('unreconciled', 'Un-reconciled'),
    ], string="Default closing type", required=True, default='unreconciled')
    account_type_id = fields.Many2one(
        comodel_name='account.account.type', string="Account type",
        required=True)
