#  -*- coding: utf-8 -*-
#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo import fields

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo.exceptions import ValidationError


class TestIntrastatStatement (AccountingTestCase):

    def setUp(self):
        super(TestIntrastatStatement, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.statement_model = self.env['account.intrastat.statement']

        self.account_account_model = self.env['account.account']
        self.account_account_receivable = self.account_account_model.create({
            'code': '1',
            'name': 'Debtors - (test)',
            'reconcile': True,
            'user_type_id': self.env.ref(
                'account.data_account_type_receivable').id})
        self.account_account_payable = self.account_account_model.create({
            'code': '2',
            'name': 'Creditors - (test)',
            'reconcile': True,
            'user_type_id': self.env.ref(
                'account.data_account_type_payable').id})

        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.purchase_journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]

        self.tax22_purchase = self.env['account.tax'].create({
            'name': "22% intra purchase",
            'description': "22",
            'amount': 22,
            'type_tax_use': 'purchase',
        })

        self.partner01 = self.env.ref('base.res_partner_1')
        self.partner01.vat = 'IT02780790107'
        self.partner01.property_account_receivable_id = \
            self.account_account_receivable
        self.partner01.property_account_payable_id = \
            self.account_account_payable
        self.product01 = self.env.ref('product.product_product_10')
        self.tax22_sale = self.env.ref('l10n_it_intrastat.tax_22')

        company = self.env.user.company_id
        company.partner_id.vat = 'IT03339130126'
        company.intrastat_custom_id = self.ref('l10n_it_intrastat.014100')

    def _get_intrastat_computed_bill(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner01.id,
            'type': 'in_invoice',
            'journal_id': self.purchase_journal.id,
            'account_id': self.account_account_payable.id,
            'intrastat': True,
            'invoice_line_ids': [(0, 0, {
                'name': 'service',
                'product_id': self.product01.id,
                'account_id': self.account_account_payable.id,
                'quantity': 1,
                'price_unit': 100,
                'invoice_line_tax_ids': [(6, 0, {
                    self.tax22_purchase.id
                })]
            })]
        })
        invoice.compute_taxes()
        invoice.action_invoice_open()
        invoice.compute_intrastat_lines()
        return invoice

    def _get_intrastat_computed_invoice(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner01.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.account_account_receivable.id,
            'intrastat': True,
            'invoice_line_ids': [(0, 0, {
                'name': 'service',
                'product_id': self.product01.id,
                'account_id': self.account_account_receivable.id,
                'quantity': 1,
                'price_unit': 100,
                'invoice_line_tax_ids': [(6, 0, {
                    self.tax22_sale.id
                })]
            })]
        })
        invoice.compute_taxes()
        invoice.action_invoice_open()
        invoice.compute_intrastat_lines()
        return invoice

    def test_statement_sale(self):
        invoice = self._get_intrastat_computed_invoice()

        statement = self.statement_model.create({
            'period_number':
                fields.Date.from_string(invoice.date_invoice).month,
        })

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement \
            .with_context(sale=True) \
            .generate_file_export()
        self.assertIn(invoice.partner_id.vat[2:], file_content)

    def test_statement_purchase(self):
        bill = self._get_intrastat_computed_bill()

        statement = self.statement_model.create({
            'period_number':
                fields.Date.from_string(bill.date_invoice).month,
        })

        # Check that before computation, file generation raises an exception
        # because statement is still empty
        with self.assertRaises(ValidationError):
            statement.generate_file_export()

        statement.compute_statement()
        file_content = statement \
            .with_context(purchase=True) \
            .generate_file_export()
        self.assertIn(bill.partner_id.vat[2:], file_content)

    def test_statement_export_file(self):
        invoice = self._get_intrastat_computed_invoice()

        statement = self.statement_model.create({
            'period_number':
                fields.Date.from_string(invoice.date_invoice).month,
        })
        statement.compute_statement()

        export_wizard = self.env['account.intrastat.export.file'] \
            .with_context(active_id=statement.id, sale=True) \
            .create({})
        export_wizard.act_getfile()
        file_content = base64.decodestring(export_wizard.data)
        self.assertIn(invoice.partner_id.vat[2:], file_content)
