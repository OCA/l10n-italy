# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def _set_journal_domain(self, domain):
        # aggiungo i movimenti dei giroconti dei pagamenti del journal
        # dedicato al cash_basis
        new_domain = []
        journal_id = self.env.context['vat_registry_journal_ids']
        cb_journal_id = self.env.user.company_id.tax_cash_basis_journal_id
        journal_id.append(cb_journal_id.id)

        for condition in domain:
            if condition[0] == 'move_id.journal_id':
                new_domain.append(('move_id.journal_id', 'in', journal_id))
            else:
                new_domain.append(condition)

        return new_domain

    def get_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_balance_domain(
            state_list, type_list)

        if not self.env.context.get('vat_registry_journal_ids'):
            return domain

        return self._set_journal_domain(domain)

    def get_base_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_base_balance_domain(
            state_list, type_list)

        if not self.env.context.get('vat_registry_journal_ids'):
            return domain

        return self._set_journal_domain(domain)

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
                        move_line.move_id)
                    if move_id.journal_id.id not in vat_reg_journal:
                        continue
                balance += (move_line.balance and -move_line.balance or 0)
            return balance
        else:
            return super(AccountTax, self).compute_balance(tax_or_base,
                                                           move_type)
