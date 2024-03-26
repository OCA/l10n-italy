# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import datetime

from odoo import fields
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.account.tests.account_test_classes import AccountingTestCase


class TestIntrastat(AccountingTestCase):

    def setUp(self):
        super().setUp()
        self.invoice_model = self.env['account.invoice']
        self.partner01 = self.env.ref('base.res_partner_1')
        self.product01 = self.env.ref('product.product_product_10')
        self.account_account_model = self.env['account.account']
        self.so_model = self.env['sale.order']
        self.fp_model = self.env['account.fiscal.position']
        self.partner_model = self.env['res.partner']
        self.res_currency_rate_model = self.env['res.currency.rate']

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

        partner_not_euro_country = self.env['res.country'].search(
            [
                ('name', 'ilike', 'poland')
            ],
            limit=1
        )
        partner_not_euro_country.currency_id.active = True
        self.partner_not_euro = self.partner_model.create({
            'name': "AMAZON EU s.a.r.l. (Poland)",
            'vat': "PL5262907815",
            'street': "Ul. Rondo Daszynskiego 1",
            'city': "Warsav",
            'zip': '00000',
            'country_id': partner_not_euro_country.id
        })

        self.res_currency_rate_model.create({
            'currency_id': partner_not_euro_country.currency_id.id,
            'name': fields.Date.to_string(fields.Date.today()),
            'rate': "1.0"
        })

        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]

        self.tax22 = self.env.ref('l10n_it_intrastat.tax_22')

    def _create_invoice_from_sale(self, sale):
        payment = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'delivered'
        })
        sale_context = {
            'active_id': sale.id,
            'active_ids': sale.ids,
            'active_model': 'sale.order',
            'open_invoices': True,
        }
        res = payment.with_context(sale_context).create_invoices()
        invoice = self.env['account.invoice'].browse(res['res_id'])
        return invoice

    def test_get_currency_rate_on_invoice_without_date_raise_exception(self):
        with self.assertRaises(UserError):
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

            invoice.get_currency_rate_at_invoice_date()

    def test_no_invoice_date_raise_exception_on_intrastat_line_compute(self):
        with self.assertRaises(UserError):
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

    def test_invoice_totals(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner01.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.account_account_receivable.id,
            'date_invoice': fields.Date.today(),
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
            line.amount_currency for line in invoice.intrastat_line_ids)
        self.assertEqual(total_intrastat_amount, invoice.amount_untaxed)

    def test_invoice_partner_no_euro_need_amount_currency(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner_not_euro.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.account_account_receivable.id,
            'date_invoice': fields.Date.today(),
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
        self.assertTrue(invoice.need_amount_currency)

    def test_currency_not_active_raise_exception(self):
        with self.assertRaises(UserError):
            invoice = self.invoice_model.create({
                'partner_id': self.partner_not_euro.id,
                'journal_id': self.sales_journal.id,
                'account_id': self.account_account_receivable.id,
                'date_invoice': fields.Date.today(),
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
        invoice.partner_id.country_id.currency_id.active = False
        # Compute intrastat lines
        invoice.compute_intrastat_lines()

    def test_no_currency_rate_raise_exception(self):
        currency_rate_date = fields.Date.today() - datetime.timedelta(days=1)
        with self.assertRaises(UserError):
            invoice = self.invoice_model.create({
                'partner_id': self.partner_not_euro.id,
                'journal_id': self.sales_journal.id,
                'account_id': self.account_account_receivable.id,
                'date_invoice': currency_rate_date,
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

    def test_invoice_totals_partner_no_euro(self):
        invoice = self.invoice_model.create({
            'partner_id': self.partner_not_euro.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.account_account_receivable.id,
            'date_invoice': fields.Date.today(),
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
            line.amount_currency for line in invoice.intrastat_line_ids)
        invoice_amount_currency = invoice.currency_id._convert(
            invoice.amount_untaxed,
            self.partner_not_euro.country_id.currency_id,
            invoice.company_id,
            invoice.date_invoice or fields.Date.today()
        )
        self.assertEqual(total_intrastat_amount, invoice_amount_currency)

    def test_invoice_from_sale(self):
        self.product01.invoice_policy = 'order'
        self.partner01.property_account_position_id = self.fp_model.create({
            'name': 'F.P subjected to intrastat',
            'intrastat': True,
        })
        so = self.so_model.create({
            'partner_id': self.partner01.id,
            'partner_invoice_id': self.partner01.id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product01.id,
                    'product_uom_qty': 1,
                    'product_uom': self.product01.uom_id.id,
                }),
            ]
        })
        so.action_confirm()
        invoice = self._create_invoice_from_sale(so)
        self.assertTrue(invoice.intrastat)
