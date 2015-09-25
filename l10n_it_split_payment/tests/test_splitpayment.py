# -*- coding: utf-8 -*-
##############################################################################
#
#    About license, see __openerp__.py
#
##############################################################################

from openerp.tests.common import TransactionCase


class TestSP(TransactionCase):

    def setUp(self):
        super(TestSP, self).setUp()
        self.tax_model = self.env['account.tax']
        self.invoice_model = self.env['account.invoice']
        self.term_model = self.env['account.payment.term']
        self.inv_line_model = self.env['account.invoice.line']
        self.fp_model = self.env['account.fiscal.position']
        self.tax22 = self.tax_model.create({
            'name': '22%',
            'amount': 0.22,
            })
        self.sp_fp = self.fp_model.create({
            'name': 'Split payment',
            'split_payment': True,
            })
        self.company = self.env.ref('base.main_company')
        self.company.sp_account_id = self.env.ref('account.ova')
        self.a_recv = self.env.ref('account.a_recv')
        self.sales_journal = self.env.ref('account.sales_journal')
        self.sales_journal.update_posted = True
        self.term_15_30 = self.term_model.create({
            'name': '15 30',
            'line_ids': [
                (0, 0, {
                    'value': 'procent',
                    'value_amount': 0.5,
                    'days': 15,
                }),
                (0, 0, {
                    'value': 'balance',
                    'days': 30,
                })]})

    def test_invoice(self):
        invoice = self.invoice_model.create({
            'partner_id': self.env.ref('base.res_partner_3').id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'fiscal_position': self.sp_fp.id,
            })
        inv_line = self.inv_line_model.create({
            'invoice_id': invoice.id,
            'name': 'service',
            'account_id': self.env.ref('account.o_income').id,
            'quantity': 1,
            'price_unit': 100,
            })
        inv_line.invoice_line_tax_id = self.tax22
        self.assertTrue(invoice.split_payment)
        invoice.signal_workflow('invoice_open')
        self.assertEqual(invoice.amount_sp, 22)
        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.residual, 100)
        self.assertEqual(invoice.amount_tax, 0)
        vat_line = False
        credit_line = False
        for line in invoice.move_id.line_id:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.debit, 22)
            if line.account_id.id == self.a_recv.id:
                credit_line = True
                self.assertEqual(line.debit, 100)
        self.assertTrue(vat_line)
        self.assertTrue(credit_line)
        invoice.action_cancel()

        invoice2 = self.invoice_model.create({
            'partner_id': self.env.ref('base.res_partner_3').id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'fiscal_position': self.sp_fp.id,
            'payment_term': self.term_15_30.id,
            })
        inv_line2 = self.inv_line_model.create({
            'invoice_id': invoice2.id,
            'name': 'service',
            'account_id': self.env.ref('account.o_income').id,
            'quantity': 1,
            'price_unit': 100,
            })
        inv_line2.invoice_line_tax_id = self.tax22
        invoice2.signal_workflow('invoice_open')
        self.assertEqual(invoice2.amount_sp, 22)
        self.assertEqual(invoice2.amount_total, 100)
        self.assertEqual(invoice2.residual, 100)
        self.assertEqual(invoice2.amount_tax, 0)
        vat_line = False
        credit_line_count = 0
        for line in invoice2.move_id.line_id:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.debit, 22)
            if line.account_id.id == self.a_recv.id:
                credit_line_count += 1
                self.assertEqual(line.debit, 50)
        self.assertTrue(vat_line)
        self.assertEqual(credit_line_count, 2)
