# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo import fields


class TestRegistry(AccountingTestCase):

    def test_invoice_and_report_cash1(self):
        """
        Registrazione di una fattura con iva per cassa, non pagata
        nessun dato nel registro iva
        """
        journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]
        ova = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id)
        ], limit=1)

        tax = self.env['account.tax'].create({
            'name': 'Tax 10.0',
            'amount': 10.0,
            'amount_type': 'fixed',
            'account_id': ova.id
        })

        tax_cash = self.env['account.tax'].create({
            'name': 'Tax 10.0 Cassa',
            'amount': 10.0,
            'amount_type': 'fixed',
            'account_id': ova.id,
            'use_cash_basis': True
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
            'journal_id': journal.id,
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
        self.env['account.invoice.line'].create({
            'product_id': self.env.ref('product.product_product_4').id,
            'quantity': 1.0,
            'price_unit': 50.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 50',
            'account_id': invoice_line_account,
            'invoice_line_tax_ids': [(6, 0, [tax_cash.id])],
        })

        invoice.compute_taxes()
        invoice.action_invoice_open()

        wizard = self.env['wizard.registro.iva'].create({
            'from_date': fields.Date.today(),
            'to_date': fields.Date.today(),
            'layout_type': 'supplier',
            'journal_ids': [(6, 0, [journal.id])],
            'fiscal_page_base': 0,
        })
        res = wizard.print_registro()
        html = self.env['report'].get_html(
            res['data']['ids'], 'l10n_it_vat_registries.report_registro_iva',
            res['data'])
        #
        self.assertTrue('Tax 10.0' in html)

    def test_invoice_and_report_cash2(self):
        """
        Registrazione di una fattura con iva per cassa, non pagata
        nessun dato nel registro iva
        """

        journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]

        journal_cash = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]

        settings = self.env['account.config.settings'].search([
            ('company_id', '=', 1)
            ])

        settings.write({
            'module_account_tax_cash_basis': True,
            'tax_cash_basis_journal_id': journal_cash.id})

        company = self.env['res.company'].search([('id', '=', 1)])

        company.write({
            'tax_cash_basis_journal_id': journal_cash.id})

        ovas = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id)
        ], limit=2)
        ova = ovas[0]
        ova_cash = ovas[1]
#         tax = self.env['account.tax'].create({
#             'name': 'Tax 10.0',
#             'amount': 10.0,
#             'amount_type': 'fixed',
#             'account_id': ova.id
#         })

        tax_cash = self.env['account.tax'].create({
            'name': 'Tax 10.0 Cassa',
            'amount': 10.0,
            'amount_type': 'fixed',
            'account_id': ova.id,
            'use_cash_basis': True,
            'cash_basis_account': ova_cash.id
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
            'journal_id': journal.id,
        })

        self.env['account.invoice.line'].create({
            'product_id': self.env.ref('product.product_product_4').id,
            'quantity': 1.0,
            'price_unit': 100.0,
            'invoice_id': invoice.id,
            'name': 'product that cost 100',
            'account_id': invoice_line_account,
            'invoice_line_tax_ids': [(6, 0, [tax_cash.id])],
        })

        invoice.compute_taxes()
        invoice.action_invoice_open()

        journal_cash = self.env['account.journal'].search(
            [('type', '=', 'cash')])[0]

        payment_methods = (
            journal.inbound_payment_method_ids or
            journal.outbound_payment_method_ids
            )
        payment_method_id = payment_methods and payment_methods[0] or False

        # pagamento
        vals = {'invoice_ids': [(6, 0, [invoice.id])],
                'partner_type': 'supplier',
                'payment_type': 'outbound',
                'journal_id': journal_cash.id,
                'payment_date': invoice.date_invoice,
                'partner_id': invoice.partner_id.id,
                'amount': invoice.amount_total,
                'payment_method_id': payment_method_id.id
                }
        payment = self.env['account.payment'].create(vals)
        payment.post()

        wizard = self.env['wizard.registro.iva'].create({
            'from_date': fields.Date.today(),
            'to_date': fields.Date.today(),
            'layout_type': 'supplier',
            'journal_ids': [(6, 0, [journal.id])],
            'fiscal_page_base': 0,
        })

        res = wizard.print_registro()

        self.assertTrue(invoice.move_id.id in res['data']['ids'])
