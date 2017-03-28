# -*- coding: utf-8 -*-
#
# Author: Andrea Gallina
# ©  2015 Apulia Software srl
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestInvoiceDueCost(TransactionCase):

    def _create_pterm(self):
        return self.env['account.payment.term'].create({
            'name': 'Ri.Ba. 30/60',
            'riba': True,
            'riba_payment_cost': 5.00,
            'line_ids': [
                (0, 0,
                 {'value': 'procent', 'days': 30,
                  'days2': -1, 'value_amount': 0.50}),
                (0, 0,
                 {'value': 'balance', 'days': 60,
                  'days2': -1})
            ]
        })

    def _create_pterm2(self):
        return self.env['account.payment.term'].create({
            'name': 'Ri.Ba. 30',
            'riba': True,
            'riba_payment_cost': 5.00,
            'line_ids': [
                (0, 0,
                 {'value': 'balance', 'days': 30,
                  'days2': -1})
            ]
        })

    def _account_expense(self):
        return self.env['account.account'].create({
            'code': 'demo_due_cost',
            'name': 'cashing fees',
            'type': 'other',
            'user_type': self.env.ref('account.data_account_type_income').id
        })

    def _create_service_due_cost(self):
        return self.env['product.product'].create({
            'name': 'Due Cost',
            'type': 'service',
            'property_account_income': self._account_expense(),
        })

    def _create_invoice(self):
        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        recent_date = self.env['account.invoice'].search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice
        return self.env['account.invoice'].create({
            'date_invoice': recent_date,
            'type': 'out_invoice',
            'journal_id': self.journalrec.id,
            'partner_id': self.partner.id,
            'payment_term': self.payment_term1.id,
            'account_id': self.credit_account.id,
            'invoice_line': [(
                0, 0, {
                    'name': self.product1.partner_ref,
                    'product_id': self.product1.id,
                    'quantity': 1.0,
                    'price_unit': 100.00,
                    'account_id': self.sale_account.id
                }
            )]
        })

    def setUp(self):
        super(TestInvoiceDueCost, self).setUp()
        self.partner = self.env.ref('base.res_partner_8')
        self.product1 = self.env.ref('product.product_product_33')
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.payment_term1 = self._create_pterm()
        self.payment_term2 = self._create_pterm2()
        self.service_due_cost = self._create_service_due_cost()
        self.credit_account = self.env.ref('account.a_recv')
        self.sale_account = self.env.ref('account.a_sale')
        self.invoice = self._create_invoice()
        self.invoice2 = self._create_invoice()

    def test_add_due_cost(self):
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Validate Invoice
        self.invoice.signal_workflow('invoice_open')
        # ---- Test Invoice has 2 line
        self.assertEquals(len(self.invoice.invoice_line), 3)
        # ---- Test Invoice Line for service cost
        self.assertEqual(self.invoice.invoice_line[1].product_id.id,
                         self.service_due_cost.id)
        # ---- Test Invoice Line for service cost
        self.assertEqual(self.invoice.invoice_line[2].product_id.id,
                         self.service_due_cost.id)
        # ---- Test Cost line is equal to 10.00
        self.assertEqual(
            (self.invoice.invoice_line[1].price_unit +
             self.invoice.invoice_line[2].price_unit), 10.00)

    def test_not_add_due_cost(self):
        # create 2 invoice for partner in same month on the second one no
        # due cost line expected
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Validate Invoice
        self.invoice.signal_workflow('invoice_open')

        self.invoice2.payment_term = self.payment_term2
        self.invoice2.signal_workflow('invoice_open')
        # ---- Test Invoice has 1 line, no due cost add because it's add on
        # ---- firts due for partner
        self.assertEquals(len(self.invoice2.invoice_line), 1)

    def test_delete_due_cost_line(self):
        # ---- Set Service in Company Config
        self.invoice.company_id.due_cost_service_id = self.service_due_cost.id
        # ---- Set allow cancel on invoice Journal
        self.invoice.journal_id.update_posted = True
        # ---- Validate Invoice
        self.invoice.signal_workflow('invoice_open')
        # ---- Cancel Invoice
        self.invoice.signal_workflow('invoice_cancel')
        # ---- Set to Draft
        self.invoice.action_cancel_draft()
        # Due Cost line has been unlink
        self.assertEqual(len(self.invoice.invoice_line), 1)
