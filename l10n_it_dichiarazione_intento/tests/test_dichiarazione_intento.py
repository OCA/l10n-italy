# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TestDichiarazioneIntento(TransactionCase):

    def _create_dichiarazione(self, partner, type_d):
        return self.env['dichiarazione.intento'].create({
            'partner_id': partner.id,
            'date': self.today_date.strftime('%Y-%m-%d'),
            'date_start': self.today_date.strftime('%Y-%m-%d'),
            'date_end': self.today_date.strftime('%Y-%m-%d'),
            'taxes_ids': [(6, 0, [self.tax1.id])],
            'limit_amount': 1000.00,
            'fiscal_position_id': self.fiscal_position.id,
            'type': type_d,
            'telematic_protocol': '08060120341234567-000001',
            })

    def _create_invoice(self, partner, tax=False, date=False, in_type=False):
        invoice_date = date if date else self.today_date.strftime('%Y-%m-%d')
        payment_term = self.env.ref('account.account_payment_term_advance')
        invoice_line_data = [(0, 0, {
            'product_id': self.env.ref('product.product_product_5').id,
            'quantity': 10.00,
            'account_id': self.a_cost.id if in_type else self.a_sale.id,
            'name': 'test line',
            'price_unit': 90.00,
            'invoice_line_tax_ids': [(6, 0, [tax.id])] if tax else False,
            })]
        return self.env['account.invoice'].sudo().create({
            'partner_id': partner.id,
            'date_invoice': invoice_date,
            'type': 'in_invoice' if in_type else 'out_invoice',
            'name': 'Test Invoice for Dichiarazione',
            'payment_term_id': payment_term.id,
            'account_id': self.pay_account.id if in_type else self.account.id,
            'invoice_line_ids': invoice_line_data,
            })

    def _create_refund(self, partner, tax=False, date=False, invoice=False):
        invoice_date = date if date else self.today_date.strftime('%Y-%m-%d')
        payment_term = self.env.ref('account.account_payment_term_advance')
        invoice_line_data = [(0, 0, {
            'quantity': 1.00,
            'account_id': self.a_sale.id,
            'name': 'test refund line',
            'price_unit': 100.00,
            'invoice_line_tax_ids': [(6, 0, [tax.id])] if tax else False,
            })]
        return self.env['account.invoice'].sudo().create({
            'partner_id': partner.id,
            'date_invoice': invoice_date,
            'type': 'out_refund',
            'name': 'Test Refund for Dichiarazione',
            'payment_term_id': payment_term.id,
            'account_id': self.account.id,
            'invoice_line_ids': invoice_line_data,
            'refund_invoice_id': invoice.id,
            })

    def setUp(self):

        super(TestDichiarazioneIntento, self).setUp()
        self.tax_model = self.env['account.tax']
        self.account = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable').id)
        ], limit=1)
        self.pay_account = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)
        ], limit=1)
        self.a_sale = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_revenue').id)
        ], limit=1)
        self.a_cost = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_direct_costs').id)
        ], limit=1)
        self.today_date = fields.Date.today()
        self.partner1 = self.env.ref('base.res_partner_2')
        self.partner2 = self.env.ref('base.res_partner_12')
        self.partner3 = self.env.ref('base.res_partner_10')
        self.partner4 = self.env.ref('base.res_partner_4')
        self.tax22 = self.tax_model.create({
            'name': '22%',
            'amount': 22,
        })
        self.tax10 = self.tax_model.create({
            'name': '10%',
            'amount': 10,
        })
        self.tax2 = self.tax_model.create({
            'name': '2%',
            'amount': 2,
        })
        self.tax1 = self.tax_model.create({
            'name': 'FC INC',
            'amount': 0,
            'price_include': True,
        })
        self.fiscal_position = self.env[
            'account.fiscal.position'].sudo().create({
                'name': 'Dichiarazione Test',
                'valid_for_dichiarazione_intento': True,
                'tax_ids': [(0, 0, {
                    'tax_src_id': self.tax10.id,
                    'tax_dest_id': self.tax1.id,
                    })]
                })
        self.fiscal_position_with_wrong_taxes = self.env[
            'account.fiscal.position'].sudo().create({
                'name': 'Dichiarazione Test Wrong',
                'valid_for_dichiarazione_intento': True,
                'tax_ids': [(0, 0, {
                    'tax_src_id': self.tax10.id,
                    'tax_dest_id': self.tax22.id,
                    })]
                })
        self.fiscal_position2 = self.env[
            'account.fiscal.position'].sudo().create({
                'name': 'Dichiarazione Test 2',
                'valid_for_dichiarazione_intento': False,
                'tax_ids': [(0, 0, {
                    'tax_src_id': self.tax22.id,
                    'tax_dest_id': self.tax10.id,
                    })]
                })

        self.dichiarazione1 = self._create_dichiarazione(self.partner1, 'out')
        self.dichiarazione2 = self._create_dichiarazione(self.partner2, 'out')
        self.dichiarazione3 = self._create_dichiarazione(self.partner2, 'out')
        self.env['dichiarazione.intento.yearly.limit'].create({
            'year': self.today_date.year,
            'limit_amount': 50000.0,
            'company_id': self.env.user.company_id.id,
        })
        self.dichiarazione4 = self._create_dichiarazione(self.partner4, 'in')
        self.invoice1 = self._create_invoice(self.partner1)
        self.invoice1.journal_id.update_posted = True
        self.invoice2 = self._create_invoice(self.partner1, tax=self.tax1)
        self.invoice3 = self._create_invoice(self.partner1, tax=self.tax1)
        self.invoice_without_valid_taxes = self._create_invoice(
            self.partner1, tax=self.tax2)
        future_date = datetime.today() + timedelta(days=10)
        future_date = future_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        self.invoice_future = self._create_invoice(self.partner1,
                                                   date=future_date,
                                                   tax=self.tax1)
        self.refund1 = self._create_refund(self.partner1, tax=self.tax1,
                                           invoice=self.invoice2)
        self.invoice4 = self._create_invoice(self.partner3, tax=self.tax22)
        self.invoice4.fiscal_position_id = self.fiscal_position2.id
        self.invoice5 = self._create_invoice(self.partner4, tax=self.tax1, in_type=True)
        self.other_company = self.env['res.company'].create({
            'name': 'other',
        })
        self.other_user = self.env['res.users'].create({
            'name': "User of other company",
            'login': "other",
            'company_ids': [
                (4, self.other_company.id),
            ],
            'company_id': self.other_company.id,
        })

    def test_dichiarazione_data(self):
        self.assertTrue(self.dichiarazione1.number)

    def test_costraints(self):
        with self.assertRaises(ValidationError):
            self.dichiarazione1.fiscal_position_id = \
                self.fiscal_position_with_wrong_taxes.id

    def test_get_valid(self):
        dichiarazione_model = self.env['dichiarazione.intento'].sudo()
        self.assertFalse(dichiarazione_model.get_valid())
        records = dichiarazione_model.get_valid(
            type_d='out', partner_id=self.partner1.id, date=self.today_date)
        self.assertEquals(len(records), 1)
        records = dichiarazione_model.get_valid(
            type_d='out', partner_id=self.partner2.id, date=self.today_date)
        self.assertEquals(len(records), 2)

    def test_dichiarazione_state_change(self):
        self.assertEqual(self.dichiarazione1.state, 'valid')
        # ----- Close dichiarazione by moving end date before today
        previuos_date = datetime.today() - timedelta(days=10)
        self.dichiarazione1.date_start = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        self.dichiarazione1.date_end = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        self.assertEqual(self.dichiarazione1.state, 'expired')

    def test_invoice_validation_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_future.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_without_valid_taxes.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_reopen_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_invoice_open()
        self.invoice1.action_invoice_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_under_dichiarazione_limit(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_over_dichiarazione_limit(self):
        self.invoice2.action_invoice_open()
        with self.assertRaises(UserError):
            self.invoice3.action_invoice_open()

    def test_invoice_reopen_with_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_invoice_open()
        self.invoice2.action_invoice_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_refund(self):
        self.invoice2.action_invoice_open()
        previous_used_amount = self.dichiarazione1.used_amount
        self.refund1.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_refund_with_amount_bigger_than_residual(self):
        self.invoice2.action_invoice_open()
        self.refund1.invoice_line_ids[0].quantity = 10

        # Check that base amount has been updated
        self.assertNotEqual(self.refund1.tax_line_ids[0].base, 1000)
        self.refund1.tax_line_ids._compute_base_amount()
        self.assertEqual(self.refund1.tax_line_ids[0].base, 1000)

        # Refund goes over plafond: 100 + 1000 > 1000
        self.assertEqual(self.dichiarazione1.available_amount, 100)
        self.assertEqual(self.refund1.amount_untaxed, 1000)
        self.assertEqual(self.dichiarazione1.limit_amount, 1000)
        with self.assertRaises(UserError):
            self.refund1.action_invoice_open()

    def test_fiscal_position_no_dichiarazione(self):
        self.invoice4._onchange_date_invoice()
        self.assertEqual(self.invoice4.fiscal_position_id.id, self.fiscal_position2.id)

    def test_invoice_vendor_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione4.used_amount
        self.assertAlmostEqual(previous_used_amount, 0.0, 2)
        self.invoice5.action_invoice_open()
        post_used_amount = self.dichiarazione4.used_amount
        self.assertAlmostEqual(post_used_amount, 900.0, 2)

    def test_copy_dichiarazione_in(self):
        dichiarazione_copy = self.dichiarazione4.copy()
        self.assertTrue(dichiarazione_copy)

    def test_multi_company(self):
        """Check that a user can only see and create declarations in his company."""
        self.env = self.env(user=self.other_user)
        declaration_model = self.env['dichiarazione.intento']

        # See only declarations in current company
        self.assertFalse(declaration_model.search_count([]))

        # Created declaration is in current company
        declaration = self._create_dichiarazione(self.partner1, 'out')
        self.assertEqual(declaration_model.search([]), declaration)
        self.assertEqual(self.env.user.company_id, declaration.company_id)
