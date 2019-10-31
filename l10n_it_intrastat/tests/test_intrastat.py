# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestIntrastat(AccountingTestCase):

    def setUp(self):
        super().setUp()
        self.invoice_model = self.env['account.invoice']
        self.partner01 = self.env.ref('base.res_partner_1')
        self.product01 = self.env.ref('product.product_product_10')
        self.account_account_model = self.env['account.account']

        self.account_account_receivable = self.account_account_model.create({
            'code': '1',
            'name': 'Debtors - (test)',
            'reconcile': True,
            'user_type_id': self.env.ref('account.data_account_type_receivable').id})

        self.account_account_payable = self.account_account_model.create({
            'code': '2',
            'name': 'Creditors - (test)',
            'reconcile': True,
            'user_type_id': self.env.ref('account.data_account_type_payable').id})

        self.partner01.property_account_receivable_id = self.account_account_receivable
        self.partner01.property_account_payable_id = self.account_account_payable

        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]

        self.tax22 = self.env.ref('l10n_it_intrastat.tax_22')

    def test_invoice_totals(self):
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
                    self.tax22.id
                })]
            })]
        })

        invoice.compute_taxes()
        invoice.action_invoice_open()

        # Compute intrastat lines
        invoice.compute_intrastat_lines()
        self.assertEqual(invoice.intrastat, True)
        # Amount Control
        total_intrastat_amount = sum(
            l.amount_currency for l in invoice.intrastat_line_ids)
        self.assertEqual(total_intrastat_amount, invoice.amount_untaxed)
