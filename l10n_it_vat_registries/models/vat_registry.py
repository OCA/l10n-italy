# -*- coding: utf-8 -*-
# Copyright 2016-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools.misc import formatLang
from odoo.tools.translate import _
import time


class ReportRegistroIva(models.AbstractModel):
    _name = 'report.l10n_it_vat_registries.report_registro_iva'

    @api.model
    def render_html(self, docids, data=None):
        # docids required by caller but not used
        # see addons/account/report/account_balance.py

        lang_code = self._context.get('company_id',
                                      self.env.user.company_id.partner_id.lang)
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format

        docargs = {
            'doc_ids': data['ids'],
            'doc_model': self.env['account.move'],
            'data': data['form'],
            'docs': self.env['account.move'].browse(data['ids']),
            'get_move': self._get_move,
            'tax_lines': self._get_tax_lines,
            'format_date': self._format_date,
            'from_date': self._format_date(
                data['form']['from_date'], date_format),
            'to_date': self._format_date(
                data['form']['to_date'], date_format),
            'registry_type': data['form']['registry_type'],
            'invoice_total': self._get_move_total,
            'tax_registry_name': data['form']['tax_registry_name'],
            'env': self.env,
            'formatLang': formatLang,
            'compute_totals_tax': self._compute_totals_tax,
            'l10n_it_count_fiscal_page_base': data['form']['fiscal_page_base'],
            'only_totals': data['form']['only_totals'],
            'date_format': date_format
        }

        return self.env['report'].render(
            'l10n_it_vat_registries.report_registro_iva', docargs)

    def _get_move(self, move_ids):
        move_list = self.env['account.move'].browse(move_ids)
        return move_list

    def _format_date(self, my_date, date_format):
        formatted_date = time.strftime(date_format,
                                       time.strptime(my_date, '%Y-%m-%d'))
        return formatted_date or ''

    def _get_tax_name(self, tax):
        name = tax.name
        if tax.parent_tax_ids and len(tax.parent_tax_ids) == 1:
            name = tax.parent_tax_ids[0].name
        return name

    def _get_invoice_from_move(self, move):
        return self.env['account.invoice'].search([
            ('move_id', '=', move.id)])

    def _tax_amounts_by_tax_id(self, move, registry_type):
        res = {}

        for move_line in move.line_ids:
            set_cee_absolute_value = False
            if not(move_line.tax_line_id or move_line.tax_ids):
                continue

            if move_line.tax_ids and len(move_line.tax_ids) != 1:
                    raise Exception(
                        _("Move line %s has too many base taxes")
                        % move_line.name)

            if move_line.tax_ids:
                tax = move_line.tax_ids[0]
                is_base = True
            else:
                tax = move_line.tax_line_id
                is_base = False

            if (
                (registry_type == 'customer' and tax.cee_type == 'sale') or
                (registry_type == 'supplier' and tax.cee_type == 'purchase')
            ):
                set_cee_absolute_value = True

            elif tax.cee_type:
                continue

            if tax.parent_tax_ids and len(tax.parent_tax_ids) == 1:
                # we group by main tax
                tax = tax.parent_tax_ids[0]

            if tax.exclude_from_registries:
                continue

            if not res.get(tax.id):
                res[tax.id] = {
                    'name': tax.name,
                    'base': 0,
                    'tax': 0,
                }
            tax_amount = move_line.debit - move_line.credit

            if set_cee_absolute_value:
                tax_amount = abs(tax_amount)

            if (
                'receivable' in move.move_type or
                ('payable_refund' == move.move_type and tax_amount > 0)
            ):
                # otherwise refund would be positive and invoices
                # negative.
                # We also check payable_refund as it normaly is < 0, but
                # it can be > 0 in case of reverse charge with VAT integration
                tax_amount = -tax_amount

            if is_base:
                # recupero il valore dell'imponibile
                res[tax.id]['base'] += tax_amount
            else:
                # recupero il valore dell'imposta
                res[tax.id]['tax'] += tax_amount

        return res

    def _get_tax_lines(self, move, data):
        """

        Args:
            move: the account.move representing the invoice

        Returns:
            A tuple of lists: (INVOICE_TAXES, TAXES_USED)
            where INVOICE_TAXES is a list of dict
            and TAXES_USED a recordset of account.tax

        """
        inv_taxes = []
        used_taxes = self.env['account.tax']

        # index è usato per non ripetere la stampa dei dati fattura quando ci
        # sono più codici IVA
        index = 0
        invoice = self._get_invoice_from_move(move)
        if 'refund' in move.move_type:
            invoice_type = "NC"
        else:
            invoice_type = "FA"

        amounts_by_tax_id = self._tax_amounts_by_tax_id(
            move, data['registry_type'])
        for tax_id in amounts_by_tax_id:
            tax = self.env['account.tax'].browse(tax_id)
            tax_item = {
                'tax_code_name': self._get_tax_name(tax),
                'base': amounts_by_tax_id[tax_id]['base'],
                'tax': amounts_by_tax_id[tax_id]['tax'],
                'index': index,
                'invoice_type': invoice_type,
                'invoice_date': (
                    invoice and invoice.date_invoice or move.date or ''),
                'reference': (
                    invoice and invoice.reference or ''),
            }
            inv_taxes.append(tax_item)
            index += 1
            used_taxes |= tax

        return inv_taxes, used_taxes

    def _get_move_total(self, move):
        total = 0.0
        receivable_payable_found = False
        for move_line in move.line_ids:
            if move_line.account_id.internal_type == 'receivable':
                total += move_line.debit or (- move_line.credit)
                receivable_payable_found = True
            elif move_line.account_id.internal_type == 'payable':
                total += (- move_line.debit) or move_line.credit
                receivable_payable_found = True
        if receivable_payable_found:
            total = abs(total)
        else:
            total = abs(move.amount)
        if 'refund' in move.move_type:
            total = -total
        return total

    def _compute_totals_tax(self, tax, data):
        """

        Args:
            tax: The tax to compute the totals for

        Returns:
            A tuple: (tax_name, base, tax, deductible, undeductible)

        """
        context = {
            'from_date': data['from_date'],
            'to_date': data['to_date'],
            'vat_registry_journal_ids': data['journal_ids'],
        }

        tax = self.env['account.tax'].with_context(context).browse(tax.id)
        tax_name = self._get_tax_name(tax)
        if not tax.children_tax_ids:
            return (
                tax_name, abs(tax.base_balance), abs(tax.balance),
                abs(tax.balance), 0
            )
        else:
            base_balance = tax.base_balance

            tax_balance = 0
            deductible = 0
            undeductible = 0
            for child in tax.children_tax_ids:
                child_balance = child.balance
                if (
                    (
                        data['registry_type'] == 'customer' and
                        child.cee_type == 'sale'
                    ) or
                    (
                        data['registry_type'] == 'supplier' and
                        child.cee_type == 'purchase'
                    )
                ):
                    # Prendo la parte di competenza di ogni registro e lo
                    # sommo sempre
                    child_balance = abs(child_balance)

                elif child.cee_type:
                    continue

                tax_balance += child_balance
                if child.account_id:
                    deductible += child_balance
                else:
                    undeductible += child_balance
            return (
                tax_name, abs(base_balance), abs(tax_balance), abs(deductible),
                abs(undeductible)
            )
