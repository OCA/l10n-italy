#  -*- coding: utf-8 -*-
#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestWithholdingTax(TransactionCase):

    def setUp(self):
        super(TestWithholdingTax, self).setUp()
        journal_misc = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        account_payable = self.env['account.account'].create({
            'name': 'Test WH tax',
            'code': 'whtaxpay',
            'user_type_id': self.ref('account.data_account_type_payable'),
            'reconcile': True})
        account_receivable = self.env['account.account'].create({
            'name': 'Test WH tax',
            'code': 'whtaxrec',
            'user_type_id': self.ref('account.data_account_type_receivable'),
            'reconcile': True})
        self.wh_tax = self.env['withholding.tax'].create({
            'name': "Test WH tax",
            'code': "Test WH tax",
            'account_receivable_id': account_receivable.id,
            'account_payable_id': account_payable.id,
            'journal_id': journal_misc.id,
            'payment_term': self.ref('account.account_payment_term_advance')
        })

    def test_overlapping_rates(self):
        """Check that overlapping rates cannot be created"""
        self.wh_tax.rate_ids = [(0, 0, {
            'date_start': fields.Date.to_string(
                date.today())
        })]
        with self.assertRaises(ValidationError):
            self.wh_tax.rate_ids = [(0, 0, {
                'date_start': fields.Date.to_string(
                    date.today() - timedelta(days=1))
            })]
