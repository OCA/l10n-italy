# -*- coding: utf-8 -*-
# Copyright 2011-2013 Associazione OpenERP Italia
# (<http://www.openerp-italia.org>).
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://http://www.linkgroup.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountTax(models.Model):
    _inherit = "account.tax"

    def get_balance_domain(self, state_list, type_list):
        domain = [
            ('move_id.state', 'in', state_list),
            ('tax_line_id', '=', self.id),
            ('tax_exigible', '=', True)
        ]
        if type_list:
            domain.append(('move_id.move_type', 'in', type_list))

        if self.env.context.get('vat_registry_journal_ids'):
            journal_id =self.env.context['vat_registry_journal_ids']
            # aggiungo i movimenti dei giroconti dei pagamenti del journal
            # dedicato al cash_basis
            cb_journal_id = self.env.user.company_id.tax_cash_basis_journal_id
            if cb_journal_id.id not in journal_id:
                journal_id.append(cb_journal_id.id)
            domain.append(
                          ('move_id.journal_id', 'in', journal_id),
                          )
        return domain

    def get_base_balance_domain(self, state_list, type_list):
        domain = [
            ('move_id.state', 'in', state_list),
            ('tax_ids', 'in', self.id),
            ('tax_exigible', '=', True)
        ]
        if type_list:
            domain.append(('move_id.move_type', 'in', type_list))
        if self.env.context.get('vat_registry_journal_ids'):
            journal_id = self.env.context['vat_registry_journal_ids']
            cb_journal_id = self.env.user.company_id.tax_cash_basis_journal_id
            if cb_journal_id.id not in journal_id:
                journal_id.append(cb_journal_id.id)
            domain.append(
                          ('move_id.journal_id', 'in', journal_id)
                          )
        return domain

    def _get_move_invoice_from_reconcilie(self, move_id):
        move_line_id = move_id.tax_cash_basis_rec_id.credit_move_id
        if move_line_id.invoice_id:
            return move_line_id.move_id
        move_line_id = move_id.tax_cash_basis_rec_id.debit_move_id
        if move_line_id.invoice_id:
            return move_line_id.move_id

        return None

    def compute_balance(self, tax_or_base='tax', move_type=None):
        self.ensure_one()
        domain = self.get_move_lines_domain(
            tax_or_base=tax_or_base, move_type=move_type)
        # balance is debit - credit whereas on tax return you want to see what
        # vat has to be paid so:
        # VAT on sales (credit) - VAT on purchases (debit).

        vat_reg_journal = self.env.context.get('vat_registry_journal_ids')
        if vat_reg_journal:
            balance = 0
            # devo prendere solo i movimenti di giroconto relativi ai journal
            # selezionati dall'utente
            for move_line in self.env['account.move.line'].search(domain):
                if move_line.move_id.tax_cash_basis_rec_id:
                    move_id = self._get_move_invoice_from_reconcilie(
                                                move_line.move_id
                                                )
                    if move_id.journal_id.id not in vat_reg_journal:
                        continue
                balance += (move_line.balance and -move_line.balance or 0)
            return balance
        else:
            balance = self.env['account.move.line'].\
            read_group(domain, ['balance'], [])[0]['balance']
            return balance and -balance or 0

