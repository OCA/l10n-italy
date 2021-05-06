#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestAccountStamp (AccountingTestCase):

    def setUp(self):
        super(TestAccountStamp, self).setUp()
        self.partner_model = self.env['res.partner']
        self.product_model = self.env['product.product']
        self.invoice_model = self.env['account.invoice']
        self.tax_model = self.env['account.tax']
        self.account_model = self.env['account.account']

        self.partner = self.partner_model.create({
            'name': "Test partner for stamp",
        })
        self.product = self.product_model.create({
            'name': "Test product for stamp",
            'lst_price': 100,
        })
        self.receivable_type_id = self.ref('account.data_account_type_receivable')
        self.account_receivable = self.account_model.search([
            ('user_type_id', '=', self.receivable_type_id),
        ], limit=1)
        self.revenue_type_id = self.ref('account.data_account_type_revenue')
        self.account_revenue = self.account_model.search([
            ('user_type_id', '=', self.revenue_type_id),
        ], limit=1)

        self.income_stamp_account = self.account_model.create({
            'name': "Test account income stamp",
            'code': 'TAIS',
            'user_type_id': self.revenue_type_id,
            'reconcile': True,
        })
        self.expense_stamp_account = self.account_model.create({
            'name': "Test account expense stamp",
            'code': 'TAES',
            'user_type_id': self.receivable_type_id,
            'reconcile': True,
        })

    def test_automatic_stamp(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner.id,
            'name': 'Test invoice automatic stamp',
            'account_id': self.account_receivable.id,
            'type': 'out_invoice',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 121.0,
                'name': 'Test invoice line for stamp',
                'account_id': self.account_revenue.id,
            })],
        })
        invoice.invoice_line_ids._onchange_product_id()
        invoice.compute_taxes()
        self.assertFalse(invoice.tax_stamp)

        stamp_product = invoice.company_id.tax_stamp_product_id
        # Set the product's tax in stamp product
        # and check that invoice is now eligible for stamp
        stamp_product.stamp_apply_tax_ids = [
            (6, 0, self.product.taxes_id.ids),
        ]
        invoice.compute_taxes()
        self.assertTrue(invoice.tax_stamp)

        stamp_product.property_account_income_id = self.income_stamp_account
        stamp_product.property_account_expense_id = self.expense_stamp_account
        invoice.action_invoice_open()
        self.assertEqual(invoice.move_id.state, 'posted')

        # Check that lines for the stamp have been created in the account move
        move_lines = invoice.move_id.line_ids
        income_stamp_line = move_lines.filtered(
            lambda line: line.account_id
            == stamp_product.property_account_income_id)
        self.assertEqual(len(income_stamp_line), 1)
        expense_stamp_line = move_lines.filtered(
            lambda line: line.account_id
            == stamp_product.property_account_expense_id)
        self.assertEqual(len(expense_stamp_line), 1)
