# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
#    About License, see __openerp__.py
#


from openerp.tests.common import TransactionCase
from datetime import datetime
from dateutil.rrule import MONTHLY


class TestTax(TransactionCase):

    def setUp(self):
        super(TestTax, self).setUp()
        self.range_type = self.env['date.range.type'].create(
            {'name': 'Fiscal year',
             'company_id': False,
             'allow_overlap': False})
        generator = self.env['date.range.generator']
        generator = generator.create({
            'date_start': '%s-01-01' % datetime.now().year,
            'name_prefix': '%s-' % datetime.now().year,
            'type_id': self.range_type.id,
            'duration_count': 1,
            'unit_of_time': MONTHLY,
            'count': 12})
        generator.action_apply()
        self.tax_model = self.env['account.tax']
        self.account_model = self.env['account.account']
        self.term_model = self.env['account.payment.term']
        self.term_line_model = self.env['account.payment.term.line']
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        today = datetime.now().date()
        self.current_period = self.env['date.range'].search([
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ])
        self.vat_statement_model = self.env['account.vat.period.end.statement']
        paid_vat_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref(
                    'account.data_account_type_current_assets').id
            )
        ], limit=1).id
        received_vat_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref(
                    'account.data_account_type_current_liabilities').id
            )
        ], limit=1).id

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        self.recent_date = self.invoice_model.search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice

        self.account_tax_22 = self.tax_model.create({
            'name': '22%',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': received_vat_account,
            'type_tax_use': 'sale',
            })
        self.account_tax_22_credit = self.tax_model.create({
            'name': '22% credit',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': paid_vat_account,
            'type_tax_use': 'purchase',
            })

        self.vat_authority = self.account_model.create({
            'code': 'VAT AUTH',
            'name': 'VAT Authority',
            'reconcile': True,
            'user_type_id': self.env.ref(
                'account.data_account_type_payable').id,
            })

        self.account_payment_term = self.term_model.create({
            'name': '16 Days End of Month',
            'note': '16 Days End of Month',
            })
        self.term_line_model.create({
            'value': 'balance',
            'days': 16,
            'option': 'fix_day_following_month',
            'payment_id': self.account_payment_term.id,
            })
        self.sale_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.purchase_journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]
        self.general_journal = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]

    def test_vat_statement(self):
        out_invoice_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_receivable').id
            )
        ], limit=1).id
        in_invoice_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_payable').id
            )
        ], limit=1).id
        out_invoice_line_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_expenses').id)
        ], limit=1).id
        in_invoice_line_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id)
        ], limit=1).id

        out_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': out_invoice_account,
            'journal_id': self.sale_journal.id,
            'partner_id': self.env.ref('base.res_partner_3').id,
            'type': 'out_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': out_invoice.id,
            'account_id': out_invoice_line_account,
            'name': 'service',
            'price_unit': 100,
            'quantity': 1,
            'invoice_line_tax_ids': [(6, 0, [self.account_tax_22.id])],
            })
        out_invoice.compute_taxes()
        out_invoice.action_invoice_open()

        in_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': in_invoice_account,
            'journal_id': self.purchase_journal.id,
            'partner_id': self.env.ref('base.res_partner_4').id,
            'type': 'in_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': in_invoice.id,
            'account_id': in_invoice_line_account,
            'name': 'service',
            'price_unit': 50,
            'quantity': 1,
            'invoice_line_tax_ids': [(6, 0, [self.account_tax_22_credit.id])],
            })
        in_invoice.compute_taxes()
        in_invoice.action_invoice_open()

        self.vat_statement = self.vat_statement_model.create({
            'journal_id': self.general_journal.id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            })
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()
        self.assertEqual(self.vat_statement.authority_vat_amount, 11)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 11)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(
            len(self.vat_statement.debit_vat_account_line_ids), 1)
        self.assertEqual(
            len(self.vat_statement.credit_vat_account_line_ids), 1)
        self.vat_statement.create_move()
        self.assertEqual(self.vat_statement.state, 'confirmed')
        self.assertTrue(self.vat_statement.move_id)
        # TODO payment
