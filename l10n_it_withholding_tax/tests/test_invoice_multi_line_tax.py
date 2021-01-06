# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato (https://girhub.com/sergiocorato)

from openerp.tests.common import TransactionCase


class TestWithholdingTax(TransactionCase):

    def setUp(self):
        super(TestWithholdingTax, self).setUp()

        # Accounts
        self.bank_journal = self.env.ref('account.bank_journal')
        self.voucher_model = self.env['account.voucher']
        type_payable = self.env.ref('account.data_account_type_payable')
        type_receivable = self.env.ref('account.data_account_type_receivable')
        self.wt_account_payable = self.env['account.account'].create({
            'name': 'Debiti per ritenute da versare',
            'code': 'WT_001',
            'user_type': type_payable.id,
            'reconcile': True,
        })
        self.wt_account_payable_enasarco = self.env['account.account'].create({
            'name': 'Debiti per Enasarco',
            'code': 'WT_002',
            'user_type': type_payable.id,
            'reconcile': True,
        })
        self.wt_account_receivable = self.env['account.account'].create({
            'name': 'Crediti per ritenute da versare',
            'code': 'WT_003',
            'user_type': type_receivable.id,
            'reconcile': True,
        })
        self.wt_account_rec_enasarco = self.env['account.account'].create({
            'name': 'Crediti per Enasarco',
            'code': 'WT_004',
            'user_type': type_receivable.id,
            'reconcile': True,
        })

        self.tax22 = self.env['account.tax'].create({
            'name': '22%',
            'amount': 0.22,
            })
        # Journals
        self.journal_misc = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        self.journal_bank = self.env['account.journal'].create(
            {'name': 'Bank', 'type': 'bank', 'code': 'BNK67'})

        # Payments
        vals_payment = {
            'name': "15 GG",
            'line_ids': [
                (0, 0, {'value': 'balance', 'days': 15})
            ]
        }
        self.payment_term_15 = self.env['account.payment.term'].create(
            vals_payment)

        # Withholding tax
        wt_vals = {
            'name': 'Provision',
            'certification': True,
            'code': 'PROV',
            'journal_id': self.journal_misc.id,
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'payment_term': self.payment_term_15.id,
            'rate_ids': [(0, 0, {'tax': 23, 'base': 0.2})]
            }
        self.wt1040 = self.env['withholding.tax'].create(wt_vals)
        # Enasarco tax
        ena_vals = {
            'name': 'Enasarco',
            'certification': True,
            'code': 'ENA',
            'wt_types': 'enasarco',
            'journal_id': self.journal_misc.id,
            'account_receivable_id': self.wt_account_rec_enasarco.id,
            'account_payable_id': self.wt_account_payable_enasarco.id,
            'payment_term': self.payment_term_15.id,
            'rate_ids': [(0, 0, {'tax': 1, 'base': 1})]
        }
        self.ena = self.env['withholding.tax'].create(ena_vals)

        self.fp = self.env['account.fiscal.position'].create({
            'name': 'Italy wt 23% on 20% Enasarco 1%',
            'withholding_tax_ids': [(6, 0, [self.ena.id, self.wt1040.id])],
        })
        # Customer Invoice with WT
        invoice_line_vals = [
            (0, 0, {
                'quantity': 1.0,
                'account_id': self.env['account.account'].search(
                    [('user_type', '=', self.env.ref(
                        'account.data_account_type_income').id)],
                    limit=1).id,
                'name': 'Provvision',
                'price_unit': 1000.00,
                'invoice_line_tax_id': [(6, 0, [self.tax22.id])],
                'invoice_line_tax_wt_ids': [(6, 0, [self.wt1040.id, self.ena.id])],
                })]
        self.recent_date = self.env['account.invoice'].search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice
        self.invoice = self.env['account.invoice'].create({
            'name': "Test Customer Invoice WT",
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'sale')])[0].id,
            'partner_id': self.env.ref('base.res_partner_12').id,
            'account_id': self.env['account.account'].search(
                [('user_type', '=', self.env.ref(
                    'account.data_account_type_receivable').id)],
                limit=1, order='id').id,
            'invoice_line': invoice_line_vals,
            'type': 'out_invoice',
            'fiscal_position': self.fp.id,
            'withholding_tax': True,
            'date_invoice': self.recent_date,
        })
        self.invoice._onchange_invoice_line_wt_ids()
        self.invoice.signal_workflow('invoice_open')

    def test_10_withholding_tax(self):
        domain = [('name', '=', 'Provision')]
        wts = self.env['withholding.tax'].search(domain)
        self.assertEqual(len(wts), 1, msg="Withholding tax was not created")

        domain = [('name', '=', 'Enasarco')]
        ena = self.env['withholding.tax'].search(domain)
        self.assertEqual(len(ena), 1, msg="Enasarco tax was not created")

        self.assertEqual(
            self.invoice.withholding_tax_amount, 56, msg='Invoice WT amount')
        self.assertEqual(
            self.invoice.amount_net_pay, 1164, msg='Invoice WT amount net pay')

        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(
            len(wt_statement), 1, msg='WT statement was not created')
        self.assertEqual(
            wt_statement.base, 200, msg='WT statement Base amount')
        self.assertEqual(
            wt_statement.amount, 0, msg='WT statement amount applied')
        self.assertEqual(
            wt_statement.amount_paid, 0, msg='WT statement Base paid')

        self.assertEqual(self.invoice.amount_net_pay, 1164)
        # pay totally
        res = self.invoice.invoice_pay_customer()
        vals = {
            'partner_id': res['context']['default_partner_id'],
            'amount': res['context']['default_amount'],
            'reference': res['context']['default_reference'],
            'type': res['context']['default_type'],
            'journal_id': self.bank_journal.id,
            'account_id': self.bank_journal.default_debit_account_id.id,
        }
        vals.update(self.voucher_model.with_context(
            res['context']
        ).recompute_voucher_lines(
            self.invoice.partner_id.id, self.bank_journal.id,
            res['context']['default_amount'], self.invoice.currency_id.id,
            'receipt', False)['value'])
        vals['line_cr_ids'] = [(0, 0, vals['line_cr_ids'][0])]
        voucher = self.voucher_model.with_context(res['context']).create(vals)
        voucher.signal_workflow('proforma_voucher')
        self.assertEqual(self.invoice.state, 'paid')
        # WT payment generation
        self.assertEqual(
            len(self.invoice.payment_ids), 1,
            msg='Missing WT payment')

        # WT amount in payment move lines
        self.assertTrue(
            set(self.invoice.payment_ids[0].move_id.line_id.mapped('debit')) ==
            set([0, 10, 1164, 46])
        )

        # WT amount applied in statement
        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(wt_statement.base, 200)
        self.assertEqual(wt_statement.tax, 46)

        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.ena.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(wt_statement.base, 1000)
        self.assertEqual(wt_statement.tax, 10)

        self.assertEqual(self.invoice.state, 'paid')
        self.assertEqual(self.invoice.amount_net_pay, 1164)
        self.assertEqual(self.invoice.residual, 0)

    def test_20_partial_payment(self):
        self.assertEqual(self.invoice.amount_net_pay, 1164)
        # pay partially
        res = self.invoice.invoice_pay_customer()
        vals = {
            'partner_id': res['context']['default_partner_id'],
            'amount': res['context']['default_amount'],
            'reference': res['context']['default_reference'],
            'type': res['context']['default_type'],
            'journal_id': self.bank_journal.id,
            'account_id': self.bank_journal.default_debit_account_id.id,
        }
        vals.update(self.voucher_model.with_context(
            res['context']
        ).recompute_voucher_lines(
            self.invoice.partner_id.id, self.bank_journal.id,
            res['context']['default_amount'] / 2, self.invoice.currency_id.id,
            'receipt', False)['value'])
        vals['line_cr_ids'] = [(0, 0, vals['line_cr_ids'][0])]
        voucher = self.voucher_model.with_context(res['context']).create(vals)
        voucher.signal_workflow('proforma_voucher')

        # WT payment generation
        self.assertEqual(
            len(self.invoice.payment_ids), 1,
            msg='Missing WT payment')

        # WT amount in payment move lines
        payment = self.invoice.payment_ids[0]
        self.assertTrue(
            set(payment.move_id.line_id.mapped('debit')) ==
            set([0, 5, 1164, 23, 0])
        )

        # WT amount applied in statement
        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.wt1040.id)]
        wt_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(wt_statement.base, 200)
        self.assertEqual(wt_statement.move_ids[0].amount, 23)

        domain = [('invoice_id', '=', self.invoice.id),
                  ('withholding_tax_id', '=', self.ena.id)]
        ena_statement = self.env['withholding.tax.statement'].search(domain)
        self.assertEqual(ena_statement.base, 1000)
        self.assertEqual(ena_statement.move_ids[0].amount, 5)

        self.assertEqual(self.invoice.state, 'open')
        self.assertEqual(self.invoice.amount_net_pay, 1164)
        self.assertEqual(self.invoice.residual, 610)

        # pay totally
        res1 = self.invoice.invoice_pay_customer()
        vals1 = {
            'partner_id': res1['context']['default_partner_id'],
            'amount': res1['context']['default_amount'],
            'reference': res1['context']['default_reference'],
            'type': res1['context']['default_type'],
            'journal_id': self.bank_journal.id,
            'account_id': self.bank_journal.default_debit_account_id.id,
        }
        vals1.update(self.voucher_model.with_context(
            res1['context']
        ).recompute_voucher_lines(
            self.invoice.partner_id.id, self.bank_journal.id,
            res1['context']['default_amount'] / 2, self.invoice.currency_id.id,
            'receipt', False)['value'])
        vals1['line_cr_ids'] = [(0, 0, vals1['line_cr_ids'][0])]
        vals1['line_dr_ids'] = [(0, 0, vals1['line_dr_ids'][0])]
        voucher1 = self.voucher_model.with_context(res1['context']).create(
            vals1)
        voucher1.signal_workflow('proforma_voucher')
        self.assertEqual(self.invoice.state, 'paid')
        # WT payment generation
        self.assertEqual(
            len(self.invoice.payment_ids), 2,
            msg='Missing WT payment')

        # WT amount in payment move lines
        payment_1 = self.invoice.payment_ids.filtered(lambda x: x != payment)
        self.assertTrue(
            set(payment_1.move_id.line_id.mapped('debit')) ==
            set([0, 5, 1164, 23, 0])
        )

        # WT amount applied in statement
        self.assertEqual(wt_statement.base, 200)
        self.assertEqual(wt_statement.move_ids[1].amount, 23)

        self.assertEqual(ena_statement.base, 1000)
        self.assertEqual(ena_statement.move_ids[1].amount, 5)

        self.assertEqual(self.invoice.state, 'paid')
        self.assertEqual(self.invoice.amount_net_pay, 1164)
        self.assertEqual(self.invoice.residual, 0)
