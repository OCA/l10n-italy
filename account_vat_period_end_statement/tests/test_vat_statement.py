# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 Agile Business Group <http://www.agilebg.com>
#    About License, see __openerp__.py
#


from openerp.tests.common import TransactionCase


class TestTax(TransactionCase):

    def setUp(self):
        super(TestTax, self).setUp()
        self.tax_model = self.env['account.tax']
        self.tax_code_model = self.env['account.tax.code']
        self.account_model = self.env['account.account']
        self.term_model = self.env['account.payment.term']
        self.term_line_model = self.env['account.payment.term.line']
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.period_model = self.env['account.period']
        self.current_period = self.period_model.find()
        self.vat_statement_model = self.env['account.vat.period.end.statement']

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        self.recent_date = self.invoice_model.search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice

        self.account_tax_code_22 = self.tax_code_model.create({
            'name': '22%',
            'vat_statement_type': 'debit',
            'vat_statement_account_id': self.env.ref('account.ova').id,
            })
        self.account_tax_code_22_imp = self.tax_code_model.create({
            'name': '22% IMP',
            })
        self.account_tax_code_22_credit = self.tax_code_model.create({
            'name': '22% credit',
            'vat_statement_type': 'credit',
            'vat_statement_account_id': self.env.ref('account.iva').id,
            })
        self.account_tax_code_22_imp_credit = self.tax_code_model.create({
            'name': '22% IMP credit',
            })

        self.account_tax_22 = self.tax_model.create({
            'name': '22%',
            'amount': 0.22,
            'tax_code_id': self.account_tax_code_22.id,
            'base_code_id': self.account_tax_code_22_imp.id,
            })
        self.account_tax_22_credit = self.tax_model.create({
            'name': '22% credit',
            'amount': 0.22,
            'tax_code_id': self.account_tax_code_22_credit.id,
            'base_code_id': self.account_tax_code_22_imp_credit.id,
            })

        self.vat_authority = self.account_model.create({
            'code': 'VAT AUTH',
            'name': 'VAT Authority',
            'parent_id': self.env.ref('account.cli').id,
            'type': 'payable',
            'reconcile': True,
            'user_type': self.env.ref('account.data_account_type_payable').id,
            })

        self.account_payment_term = self.term_model.create({
            'name': '16 Days End of Month',
            'note': '16 Days End of Month',
            })
        self.term_line_model.create({
            'value': 'balance',
            'days': 16,
            'days2': -1,
            'payment_id': self.account_payment_term.id,
            })

    def test_vat_statement(self):
        out_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': self.env.ref('account.a_recv').id,
            'journal_id': self.env.ref('account.sales_journal').id,
            'partner_id': self.env.ref('base.res_partner_3').id,
            'type': 'out_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': out_invoice.id,
            'account_id': self.env.ref('account.a_sale').id,
            'name': 'service',
            'price_unit': 100,
            'quantity': 1,
            'invoice_line_tax_id': [(6, 0, [self.account_tax_22.id])],
            })
        out_invoice.signal_workflow('invoice_open')

        in_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': self.env.ref('account.a_pay').id,
            'journal_id': self.env.ref('account.expenses_journal').id,
            'partner_id': self.env.ref('base.res_partner_4').id,
            'type': 'in_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': in_invoice.id,
            'account_id': self.env.ref('account.a_expense').id,
            'name': 'service',
            'price_unit': 50,
            'quantity': 1,
            'invoice_line_tax_id': [(6, 0, [self.account_tax_22_credit.id])],
            })
        in_invoice.signal_workflow('invoice_open')

        self.vat_statement = self.vat_statement_model.create({
            'journal_id': self.env.ref('account.miscellaneous_journal').id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            })
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()
        self.assertEqual(self.vat_statement.authority_vat_amount, 11)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 11)
        self.assertEqual(self.vat_statement.payable_vat_amount, 22)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(
            len(self.vat_statement.debit_vat_account_line_ids), 1)
        self.assertEqual(
            len(self.vat_statement.credit_vat_account_line_ids), 1)
        self.vat_statement.signal_workflow('create_move')
        self.assertEqual(self.vat_statement.state, 'confirmed')
        self.assertTrue(self.vat_statement.move_id)
        # TODO payment
