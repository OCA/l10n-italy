# -*- coding: utf-8 -*-
##############################################################################
#    
# Copyright (C) 2016 Andrea Cometa (Apulia Software)
# Email: a.cometa@apuliasoftware.it
# Web site: http://www.apuliasoftware.it
# Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2012 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo import models, fields, tools, api, _

class RibaConfiguration(models.Model):

    _name = "riba.configurazione"
    _description = "Parametri di configurazione per le Ricevute Bancarie"

    name = fields.Char("Description", size=64, required=True)
    tipo = fields.Selection(
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
        domain=[('type', '=', 'receivable')],
        help="Account used when Ri.Ba. is accepted by the bank")
    company_id = fields.Many2one(
        'res.company', "Company", required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'account.invoice'))
    accreditation_journal_id = fields.Many2one(
        'account.journal', "Accreditation journal",
        domain=[('type', '=', 'bank')],
        help="Journal used when Ri.Ba. amount is accredited by the bank")
    accreditation_account_id = fields.Many2one(
        'account.account', "Ri.Ba. bank account",
        help='Account used when Ri.Ba. is accepted by the bank')
    bank_account_id = fields.Many2one(
        'account.account', "Bank account",
        domain=[('type', '=', 'liquidity')])
    bank_expense_account_id = fields.Many2one(
        'account.account', "Bank Expenses account")
    unsolved_journal_id = fields.Many2one(
        'account.journal', "Unsolved journal",
        domain=[('type', '=', 'bank')],
        help="Journal used when Ri.Ba. is unsolved")
    overdue_effects_account_id = fields.Many2one(
        'account.account', "Overdue Effects account",
        domain=[('type', '=', 'receivable')])
    protest_charge_account_id = fields.Many2one(
        'account.account', "Protest charge account")

    def get_default_value_by_distinta(self):
        if self._context is None:
            self._context = {}
        if not self._context.get('active_id', False):
            return False
        distinta_pool = self.env['riba.distinta']
        distinta = distinta_pool.browse(
            self._cr, self._uid, self._context['active_id'],
            context=self._context)
        return distinta.config[field_name] and\
               distinta.config[field_name].id or False
    
    def get_default_value_by_distinta_line(self):
        if self._context is None:
            self._context = {}
        if not self._context.get('active_id', False):
            return False
        distinta_line = self.env['riba.distinta.line'].browse(
            self._cr, self._uid, self._context['active_id'],
            context=self._context)
        return distinta_line.distinta_id.config[field_name] and\
               distinta_line.distinta_id.config[field_name].id or False

