from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestIntrastat(AccountingTestCase):

    def setUp(self):
        super().setUp()
        self.invoice_model = self.env['account.invoice']
        self.partner01 = self.env.ref('base.res_partner_1')
        self.product01 = self.env.ref('product.product_product_10')
        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]

        self.a_recv = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_receivable').id)
        ], limit=1)
        self.a_sale = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id)
        ], limit=1)
        self.tax22 = self.env.ref('l10n_it_intrastat.tax_22')

    def test_invoice_totals(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner01.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'intrastat': True,
            'invoice_line_ids': [(0, 0, {
                'name': 'service',
                'product_id': self.product01.id,
                'account_id': self.a_sale.id,
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
