# -*- coding: utf-8 -*-
# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestL10nItWithholdingTaxPaymentOrder(TransactionCase):

    def setUp(self):
        super(TestL10nItWithholdingTaxPaymentOrder, self).setUp()
        self._create_supplier_invoice_with_wh()

    def _create_supplier_invoice_with_wh(self):
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
        # Withholding tax
        self.wt1040 = self.env['withholding.tax'].create({
            'name': 'Code 1040',
            'code': '1040',
            'certification': True,
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'journal_id': self.journal_misc.id,
            'payment_term': self.ref('account.account_payment_term_15days'),
            'rate_ids': [(0, 0, {
                    'tax': 20,
                    'base': 1,
                })]
        })
        # Supplier Invoice with WT
        self.invoice = self.env['account.invoice'].create({
            'name': 'Test invoice WT',
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'purchase')])[0].id,
            'partner_id': self.env.ref('base.res_partner_12').id,
            'account_id': self.env['account.account'].search(
                [('user_type_id', '=', self.env.ref(
                    'account.data_account_type_receivable').id)],
                limit=1, order='id').id,
            'type': 'in_invoice',
        })
        self.env['account.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'quantity': 1.0,
            'account_id': self.env['account.account'].search(
                [('user_type_id', '=', self.env.ref(
                    'account.data_account_type_expenses').id)],
                limit=1).id,
            'name': 'Test invoice line WT',
            'price_unit': 500.00,
            'invoice_line_tax_wt_ids': [(6, 0, [self.wt1040.id])]
        })
        self.invoice._onchange_invoice_line_wt_ids()

    def test_create_account_payment_line(self):
        self.invoice.action_invoice_open()
        action = self.invoice.create_account_payment_line()
        payment_order = self.env['account.payment.order'].browse(
            action['res_id'])
        self.assertEquals(len(payment_order.payment_line_ids), 1)
        self.assertEqual(
            payment_order.payment_line_ids.amount_currency,
            self.invoice.amount_net_pay)
