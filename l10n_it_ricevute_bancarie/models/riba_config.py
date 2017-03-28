# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RibaConfiguration(models.Model):

    _name = "riba.configuration"
    _description = "Configuration parameters for Ricevute Bancarie"

    name = fields.Char("Description", size=64, required=True)
    type = fields.Selection(
        (('sbf', 'Salvo buon fine'), ('incasso', 'Al dopo incasso')),
        "Modalità Emissione", required=True)
    bank_id = fields.Many2one(
        'res.partner.bank', "Banca", required=True,
        help="Bank account used for Ri.Ba. issuing")
    acceptance_journal_id = fields.Many2one(
        'account.journal', "Acceptance journal",
        domain=[('type', '=', 'bank')],
        help="Journal used when Ri.Ba. is accepted by the bank")
    acceptance_account_id = fields.Many2one(
        'account.account', "Acceptance account",
        domain=[('internal_type', '=', 'receivable')],
        help="Account used when Ri.Ba. is accepted by the bank")
    company_id = fields.Many2one(
        'res.company', "Company", required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'riba.configuration'))
    accreditation_journal_id = fields.Many2one(
        'account.journal', "Accreditation journal",
        domain=[('type', '=', 'bank')],
        help="Journal used when Ri.Ba. amount is accredited by the bank")
    accreditation_account_id = fields.Many2one(
        'account.account', "Ri.Ba. bank account",
        help='Account used when Ri.Ba. is accepted by the bank')
    bank_account_id = fields.Many2one(
        'account.account', "Bank account",
        domain=[('internal_type', '=', 'liquidity')])
    bank_expense_account_id = fields.Many2one(
        'account.account', "Bank Expenses account")
    unsolved_journal_id = fields.Many2one(
        'account.journal', "Unsolved journal",
        domain=[('type', '=', 'bank')],
        help="Journal used when Ri.Ba. is unsolved")
    overdue_effects_account_id = fields.Many2one(
        'account.account', "Overdue Effects account",
        domain=[('internal_type', '=', 'receivable')])
    protest_charge_account_id = fields.Many2one(
        'account.account', "Protest charge account")

    def get_default_value_by_list(self, field_name):
        if not self.env.context.get('active_id', False):
            return False
        ribalist_model = self.env['riba.distinta']
        ribalist = ribalist_model.browse(self.env.context['active_id'])
        return (
            ribalist.config_id[field_name] and
            ribalist.config_id[field_name].id or
            False
        )

    def get_default_value_by_list_line(self, field_name):
        if not self.env.context.get('active_id', False):
            return False
        ribalist_line = self.env['riba.distinta.line'].browse(
            self.env.context['active_id'])
        return (
            ribalist_line.distinta_id.config_id[field_name] and
            ribalist_line.distinta_id.config_id[field_name].id or
            False
        )
