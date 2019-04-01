# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestReverseCharge(TransactionCase):

    def setUp(self):
        super(TestReverseCharge, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.partner_model = self.env['res.partner']

        self._create_account()
        self._create_taxes()
        self._create_journals()
        self._create_rc_types()
        self._create_rc_type_taxes()
        self._create_fiscal_position()

        self.sample_product = self.env['product.product'].search([], limit=1)
        self.supplier_extraEU = self.partner_model.create({
            'name': 'Extra EU supplier',
            'customer': False,
            'supplier': True,
            'property_account_position_id': self.fiscal_position_extra.id
        })
        self.supplier_intraEU = self.partner_model.create({
            'name': 'Intra EU supplier',
            'customer': False,
            'supplier': True,
            'property_account_position_id': self.fiscal_position_intra.id
        })
        self.invoice_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)], limit=1).id
        self.invoice_line_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)], limit=1).id
        self.term_15_30 = self.env['account.payment.term'].create({
            'name': '15 30',
            'line_ids': [
                (0, 0, {
                    'value': 'percent',
                    'value_amount': 50,
                    'days': 15,
                    'sequence': 1,
                }),
                (0, 0, {
                    'value': 'balance',
                    'days': 30,
                    'sequence': 2,
                })]})

    def _create_account(self):
        account_model = self.env['account.account']
        self.account_selfinvoice = account_model.create({
            'code': '295000',
            'name': 'selfinvoice temporary',
            'user_type_id': self.env.ref(
                'account.data_account_type_current_liabilities').id
        })

    def _create_taxes(self):
        tax_model = self.env['account.tax']
        self.tax_22ae = tax_model.create({
            'name': "Tax 22% Purchase Extra-EU",
            'type_tax_use': 'purchase',
            'amount': 22
        })
        self.tax_22ai = tax_model.create({
            'name': "Tax 22% Purchases Intra-EU",
            'type_tax_use': 'purchase',
            'amount': 22
        })
        self.tax_22vi = tax_model.create({
            'name': "Tax 22% Sales Intra-EU",
            'type_tax_use': 'sale',
            'amount': 22
        })
        self.tax_22ve = tax_model.create({
            'name': "Tax 22% Sales Extra-EU",
            'type_tax_use': 'sale',
            'amount': 22
        })
        self.tax_22 = tax_model.create({
            'name': "Tax 22%",
            'type_tax_use': 'purchase',
            'amount': 22
        })

    def _create_journals(self):
        journal_model = self.env['account.journal']
        self.journal_selfinvoice = journal_model.create({
            'name': 'selfinvoice',
            'type': 'sale',
            'code': 'SLF',
            'update_posted': True
        })

        self.journal_reconciliation = journal_model.create({
            'name': 'RC reconciliation',
            'type': 'bank',
            'code': 'SLFRC',
            'default_credit_account_id': self.account_selfinvoice.id,
            'default_debit_account_id': self.account_selfinvoice.id,
            'update_posted': True
        })

        self.journal_selfinvoice_extra = journal_model.create({
            'name': 'Extra Selfinvoice',
            'type': 'sale',
            'code': 'SLFEX',
            'update_posted': True
        })

        self.journal_cee_extra = journal_model.create({
            'name': 'Extra CEE',
            'type': 'purchase',
            'code': 'EXCEE',
            'update_posted': True
        })

    def _create_rc_types(self):
        rc_type_model = self.env['account.rc.type']
        self.rc_type_ieu = rc_type_model.create({
            'name': 'Intra EU (selfinvoice)',
            'method': 'selfinvoice',
            'partner_type': 'supplier',
            'journal_id': self.journal_selfinvoice.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id
        })

        self.rc_type_eeu = rc_type_model.create({
            'name': 'Extra EU (selfinvoice)',
            'method': 'selfinvoice',
            'partner_type': 'other',
            'with_supplier_self_invoice': True,
            'partner_id': self.env.ref('base.main_partner').id,
            'journal_id': self.journal_selfinvoice_extra.id,
            'supplier_journal_id': self.journal_cee_extra.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id
        })

    def _create_rc_type_taxes(self):
        rc_type_tax_model = self.env['account.rc.type.tax']
        self.rc_type_tax_ieu = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_ieu.id,
            'purchase_tax_id': self.tax_22ai.id,
            'sale_tax_id': self.tax_22vi.id
        })

        self.rc_type_tax_eeu = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_eeu.id,
            'purchase_tax_id': self.tax_22ae.id,
            'sale_tax_id': self.tax_22ve.id
        })

    def _create_fiscal_position(self):
        model_fiscal_position = self.env['account.fiscal.position']
        self.fiscal_position_intra = model_fiscal_position.create({
            'name': 'Intra EU',
            'rc_type_id': self.rc_type_ieu.id
        })

        self.fiscal_position_extra = model_fiscal_position.create({
            'name': 'Extra EU',
            'rc_type_id': self.rc_type_eeu.id
        })

    def test_intra_EU_invoice_line_no_tax(self):

        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })

        invoice_line = self.invoice_line_model.create({
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100
        })
        invoice_line.onchange_invoice_line_tax_id()
        with self.assertRaises(UserError):
            invoice.action_invoice_open()

    def test_intra_EU(self):
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()

        invoice.action_invoice_open()
        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(
            bool(invoice.rc_self_invoice_id.payment_term_id), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_invoice_id.payment_move_line_ids.move_id.state,
            'posted')

    def test_intra_EU_2_mixed_lines(self):
        """Create an invoice with two lines: one is RC and the other is not.
        By default, the onchange method `onchange_invoice_line_tax_id` assigns
        the same RC flag to both lines, so we force one of them not to be RC"""
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product 1',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'Invoice for sample product 2',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 200,
            'rc': False,
            'invoice_line_tax_ids': [(4, self.tax_22.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line.rc = False

        invoice.compute_taxes()

        invoice.action_invoice_open()
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
            'type': 'in_invoice',
        })
        invoice.company_id.tax_calculation_rounding_method = 'round_globally'
        invoice_line_vals = {
            'name': 'invoice line 1',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 2.89,
            'quantity': 15,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 2',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 4.05,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 3',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 4.12,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 4',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 1.60,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 5',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 5.65,
            'quantity': 5,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 6',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 12,
            'quantity': 1,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice_line_vals = {
            'name': 'invoice line 7',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'price_unit': 0.13,
            'quantity': 1,
            'rc': True,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()

        invoice.compute_taxes()
        invoice.action_invoice_open()

        self.assertIsNot(bool(invoice.rc_self_invoice_id), False)
        self.assertIsNot(
            bool(invoice.rc_self_invoice_id.payment_term_id), True)
        self.assertEqual(invoice.rc_self_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_invoice_id.payment_move_line_ids.move_id.state,
            'posted')
        # compare amount_tax with amount show on paymenys_widget
        invoice._get_payment_info_JSON()
        info = json.loads(invoice.payments_widget)['content'][0]
        self.assertEqual(info['amount'], invoice.amount_tax)

    def test_extra_EU(self):
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_extraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()

        invoice.action_invoice_open()
        self.assertIsNot(bool(invoice.rc_self_purchase_invoice_id), False)
        self.assertEqual(invoice.rc_self_purchase_invoice_id.state, 'paid')
        self.assertEqual(
            invoice.rc_self_purchase_invoice_id.payment_move_line_ids.
            move_id.state, 'posted')

    def test_intra_EU_cancel_and_draft(self):

        invoice = self.invoice_model.create({
            'partner_id': self.supplier_intraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_invoice',
        })

        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        invoice.compute_taxes()

        invoice.action_invoice_open()

        self.env['account.journal'].search(
            [('name', '=', 'Customer Invoices')]).update_posted = True
        invoice.action_cancel()
        self.assertEqual(invoice.state, 'cancel')
        invoice.action_invoice_draft()
        self.assertEqual(invoice.state, 'draft')

    def test_new_refund_flag(self):
        """Check that the lines of a new refund have the RC flag properly set.
        """
        invoice = self.invoice_model.create({
            'partner_id': self.supplier_extraEU.id,
            'account_id': self.invoice_account,
            'type': 'in_refund',
        })
        invoice_line_vals = {
            'name': 'Invoice for sample product',
            'account_id': self.invoice_line_account,
            'invoice_id': invoice.id,
            'product_id': self.sample_product.id,
            'price_unit': 100,
            'invoice_line_tax_ids': [(4, self.tax_22ai.id, 0)]}
        invoice_line = self.invoice_line_model.create(invoice_line_vals)
        invoice_line.onchange_invoice_line_tax_id()
        self.assertTrue(all(line.rc for line in invoice.invoice_line_ids))
