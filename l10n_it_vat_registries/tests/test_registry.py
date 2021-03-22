# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.account.tests.account_test_classes import AccountingTestCase
from odoo import fields


class TestRegistry(AccountingTestCase):

    def test_invoice_and_report(self):
        test_date = fields.Date.today()
        self.journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
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
        tax_registry = self.env['account.tax.registry'].create({
            'name': 'Sales',
            'layout_type': 'customer',
            'journal_ids': [(6, 0, [self.journal.id])],
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
            'date_invoice': test_date,
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
            'from_date': test_date,
            'to_date': test_date,
            'tax_registry_id': tax_registry.id,
            'layout_type': 'supplier',
            'fiscal_page_base': 0,
        })
        wizard.on_change_tax_registry_id()
        res = wizard.print_registro()

        domain = [('report_type', 'like', 'qweb'),
                  ('report_name',
                   '=',
                   'l10n_it_vat_registries.report_registro_iva')]
        report = self.env['ir.actions.report'].search(domain)
        html = report.render_qweb_html(res['data']['ids'], res['data'])

        self.assertTrue(b'Tax 10.0' in html[0])
