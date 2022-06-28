# -*- coding: utf-8 -*-

# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2019 Alex Comba - Agile Business Group

from openerp.exceptions import Warning as UserError
from .rc_common import ReverseChargeCommon


class TestReverseCharge(ReverseChargeCommon):

    def setUp(self):
        super(TestReverseCharge, self).setUp()

    def test_intra_EU_invoice_line_no_tax(self):

        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line = self.invoice_line_model.create({
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100
        })
        invoice_line.onchange_invoice_line_tax_id()
        with self.assertRaises(UserError):
            invoice.signal_workflow('invoice_open')

    def test_intra_EU(self):
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')
        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(
            bool(invoice.rc_self_invoice_id.payment_term), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_invoice_id.payment_ids.move_id.state,
            'posted')
        self.assertTrue(
            "Intra EU supplier" in invoice.rc_self_invoice_id.comment)

    def test_intra_EU_2_mixed_lines(self):
        """Create an invoice with two lines: one is RC and the other is not.
        By default, the onchange method `onchange_invoice_line_tax_id` assigns
        the same RC flag to both lines, so we force one of them not to be RC"""
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product 1',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'Invoice for sample product 2',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 200,
            'rc': False,
            'invoice_line_tax_id': [(4, self.tax_22.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line.rc = False

        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')
        # Only the tax in the RC line (22) should result as paid
        self.assertEqual(invoice.amount_total, 366.0)
        self.assertEqual(invoice.residual, 344.0)

    def test_intra_EU_amount_tax_amount_payments_widget_discrepancy(self):
        """Create an invoice with round_globally where there was discrepancy
        between amount_tax (29.17) and amount shown on payments_widget (29.18).
        """
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']
        invoice.company_id.tax_calculation_rounding_method = 'round_globally'
        invoice_line_vals = {
            'name': 'invoice line 1',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 2.89,
            'quantity': 15,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 2',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 4.05,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 3',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 4.12,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 4',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 1.60,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 5',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 5.65,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 6',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 12,
            'quantity': 1,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 7',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 0.13,
            'quantity': 1,
            'rc': True,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()

        self.env['account.invoice.tax'].compute(invoice)
        invoice.signal_workflow('invoice_open')

        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(
            bool(invoice.rc_self_invoice_id.payment_term), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_invoice_id.payment_ids.move_id.state,
            'posted')
        # compare amount_tax with amount in the payment
        self.assertEqual(invoice.payment_ids.debit, invoice.amount_tax)

    def test_extra_EU(self):
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_extraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')
        self.assertIsNot(bool(invoice.rc_self_purchase_invoice_id), False)
        self.assertEqual(invoice.rc_self_purchase_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_purchase_invoice_id.payment_ids.
            move_id.state, 'posted')

        invoice.journal_id.update_posted = True
        invoice.signal_workflow('invoice_cancel')
        self.assertEqual(invoice.state, 'cancel')
        invoice.action_cancel_draft()
        # see what done with "with invoice.env.do_in_draft()" in
        # action_cancel_draft
        invoice.refresh()
        self.assertEqual(invoice.state, 'draft')

    def test_intra_EU_cancel_and_draft(self):

        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')

        invoice.journal_id.update_posted = True
        invoice.signal_workflow('invoice_cancel')
        self.assertEqual(invoice.state, 'cancel')
        invoice.action_cancel_draft()
        invoice.refresh()
        self.assertEqual(invoice.state, 'draft')

    def test_intra_EU_zero_total(self):

        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': -100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()

        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')
        self.assertEqual(invoice.amount_total, 0)
        self.assertEqual(invoice.rc_self_invoice_id.amount_total, 0)
        # Note that invoices with amount 0 are not automatically paid
        self.assertEqual(invoice.state, 'open')
        self.assertEqual(invoice.rc_self_invoice_id.state, 'open')

        invoice.journal_id.update_posted = True
        invoice.signal_workflow('invoice_cancel')
        self.assertEqual(invoice.state, 'cancel')
        # self invoice is only canceled when there are payments
        self.assertEqual(invoice.rc_self_invoice_id.state, 'open')
        invoice.action_cancel_draft()
        invoice.refresh()
        self.assertEqual(invoice.state, 'draft')
        self.assertEqual(invoice.rc_self_invoice_id.state, 'draft')

    def test_new_refund_flag(self):
        """Check that the lines of a new refund have the RC flag properly set.
        """
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_extraEU.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_refund',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']
        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.assertTrue(all(line.rc for line in invoice.invoice_line))

    def test_intra_EU_exempt(self):
        self.supplier_intraEU.property_payment_term = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU_exempt.id,
            'account_id': self.invoice_account,
            'journal_id': self.purchases_journal.id,
            'type': 'in_invoice',
        })
        res = invoice.onchange_partner_id(invoice.type, invoice.partner_id.id)
        invoice.fiscal_position = res['value']['fiscal_position']

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_id': [(4, self.tax_0_pur.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.env['account.invoice.tax'].compute(invoice)

        invoice.signal_workflow('invoice_open')
        self.assertEqual(invoice.amount_total, 100)
        self.assertEqual(invoice.residual, 100)
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        self.assertEqual(invoice.rc_self_invoice_id.amount_total, 100)
        self.assertEqual(invoice.rc_self_invoice_id.residual, 0)
        invoice.journal_id.update_posted = True
        invoice.signal_workflow('invoice_cancel')
        invoice.signal_workflow('invoice_cancel')

        self.assertEqual(invoice.state, 'cancel')
        invoice.action_cancel_draft()

        invoice.refresh()
        self.assertEqual(invoice.state, 'draft')
