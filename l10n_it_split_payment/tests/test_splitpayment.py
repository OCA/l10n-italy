# -*- coding: utf-8 -*-
##############################################################################
#
#    About license, see __openerp__.py
#
##############################################################################

from openerp.tests.common import TransactionCase
from openerp import netsvc


class TestSP(TransactionCase):

    def setUp(self):
        super(TestSP, self).setUp()
        cr, uid = self.cr, self.uid
        self.tax_model = self.registry('account.tax')
        self.tax_code_model = self.registry('account.tax.code')
        self.invoice_model = self.registry('account.invoice')
        self.term_model = self.registry('account.payment.term')
        self.inv_line_model = self.registry('account.invoice.line')
        self.fp_model = self.registry('account.fiscal.position')
        self.company_model = self.registry('res.company')
        self.data_model = self.registry('ir.model.data')
        self.journal_model = self.registry('account.journal')
        self.taxcode22_id = self.tax_code_model.create(cr, uid, {
            'name': '22% SP',
            })
        self.taxcode22base_id = self.tax_code_model.create(cr, uid, {
            'name': '22% SP (base)',
            })
        self.tax22_id = self.tax_model.create(cr, uid, {
            'name': '22% SP',
            'amount': 0.22,
            'tax_code_id': self.taxcode22_id,
            'base_code_id': self.taxcode22base_id,
            'ref_tax_code_id': self.taxcode22_id,
            'ref_base_code_id': self.taxcode22base_id,
            })
        self.sp_fp_id = self.fp_model.create(cr, uid, {
            'name': 'Split payment',
            'split_payment': True,
            })
        company_id = self.data_model.get_object_reference(
            cr, uid, 'base', 'main_company')[1]
        account_ova_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'ova')[1]
        self.a_recv_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'a_recv')[1]
        self.sales_journal_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'sales_journal')[1]

        self.company = self.company_model.browse(cr, uid, company_id)
        self.company.write({'sp_account_id': account_ova_id})

        self.journal_model.write(
            cr, uid, [self.sales_journal_id], {'update_posted': True})

        self.term_15_30_id = self.term_model.create(cr, uid, {
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
        cr, uid = self.cr, self.uid
        wf_service = netsvc.LocalService("workflow")
        res_partner_3_id = self.data_model.get_object_reference(
            cr, uid, 'base', 'res_partner_3')[1]
        o_income_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'o_income')[1]
        invoice_id = self.invoice_model.create(cr, uid, {
            'partner_id': res_partner_3_id,
            'journal_id': self.sales_journal_id,
            'account_id': self.a_recv_id,
            'fiscal_position': self.sp_fp_id,
            })
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.inv_line_model.create(cr, uid, {
            'invoice_id': invoice.id,
            'name': 'service',
            'account_id': o_income_id,
            'quantity': 1,
            'price_unit': 100,
            'invoice_line_tax_id': [(6, 0, [self.tax22_id])],
            })
        self.assertTrue(invoice.split_payment)
        invoice.button_compute()
        wf_service.trg_validate(
            uid, 'account.invoice', invoice.id, 'invoice_open', cr)
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
            if line.account_id.id == self.a_recv_id:
                credit_line = True
                self.assertEqual(line.debit, 100)
        self.assertTrue(vat_line)
        self.assertTrue(credit_line)
        invoice.action_cancel()

        # invoice with payment term
        invoice2_id = self.invoice_model.create(cr, uid, {
            'partner_id': res_partner_3_id,
            'journal_id': self.sales_journal_id,
            'account_id': self.a_recv_id,
            'fiscal_position': self.sp_fp_id,
            'payment_term': self.term_15_30_id,
            })
        invoice2 = self.invoice_model.browse(cr, uid, invoice2_id)
        self.inv_line_model.create(cr, uid, {
            'invoice_id': invoice2.id,
            'name': 'service',
            'account_id': o_income_id,
            'quantity': 1,
            'price_unit': 100,
            'invoice_line_tax_id': [(6, 0, [self.tax22_id])],
            })
        invoice2.button_compute()
        wf_service.trg_validate(
            uid, 'account.invoice', invoice2.id, 'invoice_open', cr)
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
            if line.account_id.id == self.a_recv_id:
                credit_line_count += 1
                self.assertEqual(line.debit, 50)
        self.assertTrue(vat_line)
        self.assertEqual(credit_line_count, 2)

        # refund
        invoice3_id = self.invoice_model.create(cr, uid, {
            'partner_id': res_partner_3_id,
            'journal_id': self.sales_journal_id,
            'account_id': self.a_recv_id,
            'fiscal_position': self.sp_fp_id,
            'type': 'out_refund',
            })
        invoice3 = self.invoice_model.browse(cr, uid, invoice3_id)
        self.inv_line_model.create(cr, uid, {
            'invoice_id': invoice3.id,
            'name': 'service',
            'account_id': o_income_id,
            'quantity': 1,
            'price_unit': 100,
            'invoice_line_tax_id': [(6, 0, [self.tax22_id])],
            })
        self.assertTrue(invoice3.split_payment)
        invoice3.button_compute()
        wf_service.trg_validate(
            uid, 'account.invoice', invoice3.id, 'invoice_open', cr)
        self.assertEqual(invoice3.amount_sp, 22)
        self.assertEqual(invoice3.amount_total, 100)
        self.assertEqual(invoice3.residual, 100)
        self.assertEqual(invoice3.amount_tax, 0)
        vat_line = False
        credit_line = False
        for line in invoice3.move_id.line_id:
            if line.account_id.id == self.company.sp_account_id.id:
                vat_line = True
                self.assertEqual(line.credit, 22)
            if line.account_id.id == self.a_recv_id:
                credit_line = True
                self.assertEqual(line.credit, 100)
        self.assertTrue(vat_line)
        self.assertTrue(credit_line)
