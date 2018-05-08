# -*- coding: utf-8 -*-
from odoo.tests import common


class TestRibaCommon(common.TransactionCase):

    def setUp(self):
        super(TestRibaCommon, self).setUp()
        self.service_due_cost = self._create_service_due_cost()
        self.account_model = self.env['account.account']
        self.move_line_model = self.env['account.move.line']
        self.move_model = self.env['account.move']
        self.distinta_model = self.env['riba.distinta']
        self.account_user_type = self.env.ref(
            'account.data_account_type_receivable')
        self.account_asset_user_type = self.env.ref(
            'account.data_account_type_fixed_assets')
        self.partner = self.env.ref('base.res_partner_3')
        self.product1 = self.env.ref('product.product_product_5')
        self.sale_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.bank_journal = self.env['account.journal'].search([
            ('type', '=', 'bank')], limit=1)
        self.payment_term1 = self._create_pterm()
        self.payment_term2 = self._create_pterm2()
        self.account_rec1_id = self.account_model.create(dict(
            code="cust_acc",
            name="customer account",
            user_type_id=self.account_user_type.id,
            reconcile=True,
        ))
        self.sale_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id
            )
        ], limit=1)
        self.expenses_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_expenses').id
            )
        ], limit=1)
        self.bank_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_liquidity').id
            )
        ], limit=1)
        self.invoice = self._create_invoice()
        self.invoice2 = self._create_invoice()
        self.sbf_effects = self.env['account.account'].create({
            'code': 'SBF',
            'name': 'SBF effects (test)',
            'reconcile': True,
            'user_type_id': self.account_user_type.id,
        })
        self.riba_account = self.env['account.account'].create({
            'code': 'RiBa',
            'name': 'RiBa account (test)',
            'user_type_id': self.account_asset_user_type.id,
        })
        self.unsolved_account = self.env['account.account'].create({
            'code': 'UNSOLVED',
            'name': 'Overdue effects account (test)',
            'reconcile': True,
            'user_type_id': self.account_user_type.id,
        })
        self.company_bank = self.env.ref(
            'l10n_it_ricevute_bancarie.company_bank')
        self.riba_config = self.create_config()
        self.account_payment_term_riba = self.env.ref(
            'l10n_it_ricevute_bancarie.account_payment_term_riba')

    def _create_service_due_cost(self):
        return self.env['product.product'].create({
            'name': 'Due Cost',
            'type': 'service',
            'property_account_income_id': self._account_expense(),
        })

    def _account_expense(self):
        return self.env['account.account'].create({
            'code': 'demo_due_cost',
            'name': 'cashing fees',
            'user_type_id': self.env.ref(
                'account.data_account_type_expenses').id
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
            'journal_id': self.sale_journal.id,
            'partner_id': self.partner.id,
            'payment_term_id': self.payment_term1.id,
            'account_id': self.account_rec1_id.id,
            'invoice_line_ids': [(
                0, 0, {
                    'name': self.product1.partner_ref,
                    'product_id': self.product1.id,
                    'quantity': 1.0,
                    'price_unit': 100.00,
                    'account_id': self.sale_account.id
                }
            )]
        })

    def _create_pterm(self):
        return self.env['account.payment.term'].create({
            'name': 'Ri.Ba. 30/60',
            'riba': True,
            'riba_payment_cost': 5.00,
            'line_ids': [
                (0, 0,
                 {'value': 'percent', 'days': 30,
                  'option': 'day_after_invoice_date', 'value_amount': 0.50}),
                (0, 0,
                 {'value': 'balance', 'days': 60,
                  'option': 'day_after_invoice_date'})
            ]
        })

    def _create_pterm2(self):
        return self.env['account.payment.term'].create({
            'name': 'Ri.Ba. 30',
            'riba': True,
            'riba_payment_cost': 5.00,
            'line_ids': [
                (0, 0,
                 {'value': 'balance', 'option': 'last_day_following_month'})
            ]
        })

    def create_config(self):
        return self.env['riba.configuration'].create({
            'name': 'Salvo Buon Fine',
            'type': 'sbf',
            'bank_id': self.company_bank.id,
            'acceptance_journal_id': self.bank_journal.id,
            'accreditation_journal_id': self.bank_journal.id,
            'acceptance_account_id': self.sbf_effects.id,
            'accreditation_account_id': self.riba_account.id,
            'bank_account_id': self.bank_account.id,
            'bank_expense_account_id': self.expenses_account.id,
            'unsolved_journal_id': self.bank_journal.id,
            'overdue_effects_account_id': self.unsolved_account.id,
            'protest_charge_account_id': self.expenses_account.id,
        })
