# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)

from odoo.tests.common import TransactionCase
from datetime import date, timedelta
from odoo import fields
from odoo.exceptions import ValidationError
import time


class TestWithholdingTax(TransactionCase):

    def setUp(self):
        super(TestWithholdingTax, self).setUp()

        # Accounts
        type_payable = self.env.ref('account.data_account_type_payable')
        type_receivable = self.env.ref('account.data_account_type_receivable')
        self.wt_account_payable = self.env['account.account'].create({
            'name': 'Debiti per ritenute da versare',
            'code': 'WT_001',
            'user_type_id': type_payable.id,
            'reconcile': True,
        })
        self.wt_account_receivable = self.env['account.account'].create({
            'name': 'Crediti per ritenute subite',
            'code': 'WT_002',
            'user_type_id': type_receivable.id,
            'reconcile': True,
        })

        # Journals
        self.journal_misc = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        self.journal_bank = self.env['account.journal'].create(
            {'name': 'Bank', 'type': 'bank', 'code': 'BNK67'})

        # Payments
        vals_payment = {
            'name': "",
            'line_ids': [(0, 0, {'value': 'balance', 'days': 15})]
            }
        self.payment_term_15 = self.env['account.payment.term'].create(
            vals_payment)

        # Withholding tax
        wt_vals = {
            'name': 'Code 1040',
            'code': '1040',
            'certification': True,
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'journal_id': self.journal_misc.id,
            'payment_term': self.payment_term_15.id,
            'rate_ids': [(0, 0, {
                    'tax': 20,
                    'base': 1,
                })]
            }
        self.wt1040 = self.env['withholding.tax'].create(wt_vals)

        # Supplier Invoice with WT
        invoice_line_vals = [
            (0, 0, {
                'quantity': 1.0,
                'account_id': self.env['account.account'].search(
                    [('user_type_id', '=', self.env.ref(
                        'account.data_account_type_expenses').id)],
                    limit=1).id,
                'name': 'Advice',
                'price_unit': 1000.00,
                'invoice_line_tax_wt_ids': [(6, 0, [self.wt1040.id])]
                })]
        self.invoice = self.env['account.invoice'].create({
            'name': "Test Supplier Invoice WT",
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'purchase')])[0].id,
            'partner_id': self.env.ref('base.res_partner_12').id,
            'account_id': self.env['account.account'].search(
                [('user_type_id', '=', self.env.ref(
                    'account.data_account_type_receivable').id)],
                limit=1, order='id').id,
            'invoice_line_ids': invoice_line_vals,
            'type': 'in_invoice',
        })
        self.invoice._onchange_invoice_line_wt_ids()
        self.invoice.action_invoice_open()

    def test_withholding_tax(self):
        domain = [('name', '=', 'Code 1040')]
        wts = self.env['withholding.tax'].search(domain)
        self.assertEqual(len(wts), 1, msg="Withholding tax was not created")

        self.assertEqual(
            self.invoice.withholding_tax_amount, 200, msg='Invoice WT amount')
        self.assertEqual(
            self.invoice.amount_net_pay, 800, msg='Invoice WT amount net pay')

        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(
            len(wt_statement), 1, msg='WT statement was not created')
        self.assertEqual(
            wt_statement.base, 1000, msg='WT statement Base amount')
        self.assertEqual(
            wt_statement.amount, 0, msg='WT statement amount applied')
        self.assertEqual(
            wt_statement.amount_paid, 0, msg='WT statement Base paid')

        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 800)

        ctx = {
            'active_model': 'account.invoice',
            'active_ids': [self.invoice.id],
            }
        register_payments = self.env['account.register.payments']\
            .with_context(ctx).create({
                'payment_date': time.strftime('%Y') + '-07-15',
                'amount': 800,
                'journal_id': self.journal_bank.id,
                'payment_method_id': self.env.ref(
                    "account.account_payment_method_manual_out").id,
                })
        register_payments.create_payments()

        # WT payment generation
        self.assertEqual(
            len(self.invoice.payment_move_line_ids), 2,
            msg='Missing WT payment')

        # WT amount in payment move lines
        self.assertTrue(
            set(self.invoice.payment_move_line_ids.mapped('debit')) ==
            set([800, 200])
        )

        # WT aomunt applied in statement
        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(wt_statement.amount, 200)
        self.assertEqual(self.invoice.state, 'paid')
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 0)

    def test_partial_payment(self):
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 800)
        ctx = {
            'active_model': 'account.invoice',
            'active_ids': [self.invoice.id],
            'active_id': self.invoice.id,
            'default_invoice_ids': [(4, self.invoice.id, None)],
            }
        register_payments = self.env['account.payment'].with_context(
            ctx
        ).create({
            'payment_date': time.strftime('%Y') + '-07-15',
            'amount': 600,
            'journal_id': self.journal_bank.id,
            'payment_method_id': self.env.ref(
                "account.account_payment_method_manual_out").id,
            })
        register_payments.action_validate_invoice_payment()

        # WT amount in payment move lines
        self.assertTrue(
            set(self.invoice.payment_move_line_ids.mapped('debit')) ==
            set([600, 150])
        )

        # WT aomunt applied in statement
        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(wt_statement.amount, 150)
        self.assertEqual(self.invoice.amount_net_pay, 800)
        self.assertEqual(self.invoice.amount_net_pay_residual, 200)
        self.assertEqual(self.invoice.residual, 250)
        self.assertEqual(self.invoice.state, 'open')

    def test_overlapping_rates(self):
        """Check that overlapping rates cannot be created"""
        with self.assertRaises(ValidationError):
            self.wt1040.rate_ids = [(0, 0, {
                'date_start': fields.Date.to_string(
                    date.today() - timedelta(days=1))
            })]

    def test_duplicating_wt(self):
        new_tax = self.wt1040.copy()
        self.assertEqual(new_tax.code, "1040 (copy)")
        self.assertEqual(new_tax.name, "Code 1040")
