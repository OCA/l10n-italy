# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo import fields


class TestRegistry(AccountingTestCase):

    def test_invoice_and_report(self):
        self.journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]
        self.ova = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id)
        ], limit=1)
        tax = self.env['account.tax'].create({
            'name': 'Tax 10.0',
            'amount': 10.0,
            'amount_type': 'fixed',
            'account_id': self.ova.id,
        })
        invoice_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_receivable').id
            )
        ], limit=1).id
        invoice_line_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_expenses').id)
        ], limit=1).id

        invoice = self.env['account.invoice'].create({
            'partner_id': self.env.ref('base.res_partner_2').id,
            'account_id': invoice_account,
            'type': 'in_invoice',
            'journal_id': self.journal.id,
        })

        self.env['account.invoice.line'].create({
            'product_id': self.env.ref('product.product_product_4').id,
            'quantity': 1.0,
            'price_unit': 100.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 100',
            'account_id': invoice_line_account,
            'invoice_line_tax_ids': [(6, 0, [tax.id])],
        })
        invoice.compute_taxes()
        invoice.action_invoice_open()

        wizard = self.env['wizard.registro.iva'].create({
            'from_date': fields.Date.today(),
            'to_date': fields.Date.today(),
            'layout_type': 'supplier',
            'journal_ids': [(6, 0, [self.journal.id])],
            'fiscal_page_base': 0,
        })
        res = wizard.print_registro()
        html = self.env['report'].get_html(
            res['data']['ids'], 'l10n_it_vat_registries.report_registro_iva',
            res['data'])
        self.assertTrue('Tax 10.0' in html)
