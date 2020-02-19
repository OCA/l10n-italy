#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from datetime import datetime, date
from dateutil.rrule import MONTHLY


class TestTax(TransactionCase):

    def setUp(self):
        super(TestTax, self).setUp()
        self.range_type = self.env['date.range.type'].create(
            {'name': 'Fiscal year',
             'company_id': False,
             'allow_overlap': False})
        generator = self.env['date.range.generator']
        generator = generator.create({
            'date_start': '%s-01-01' % datetime.now().year,
            'name_prefix': '%s-' % datetime.now().year,
            'type_id': self.range_type.id,
            'duration_count': 1,
            'unit_of_time': MONTHLY,
            'count': 12})
        generator.action_apply()
        prev_year_generator = generator.create({
            'date_start': '%s-01-01' % (datetime.now().year - 1),
            'name_prefix': '%s-' % (datetime.now().year - 1),
            'type_id': self.range_type.id,
            'duration_count': 1,
            'unit_of_time': MONTHLY,
            'count': 12})
        prev_year_generator.action_apply()
        self.tax_model = self.env['account.tax']
        self.account_model = self.env['account.account']
        self.term_model = self.env['account.payment.term']
        self.term_line_model = self.env['account.payment.term.line']
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        today = datetime.now().date()
        self.current_period = self.env['date.range'].search([
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ])
        self.last_year_date = date(today.year - 1, today.month, today.day)
        self.last_year_period = self.env['date.range'].search([
            ('date_start', '<=', self.last_year_date),
            ('date_end', '>=', self.last_year_date)
        ])
        self.vat_statement_model = self.env['account.vat.period.end.statement']
        self.paid_vat_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref(
                    'account.data_account_type_current_assets').id
            )
        ], limit=1).id
        self.received_vat_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref(
                    'account.data_account_type_current_liabilities').id
            )
        ], limit=1).id

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        self.recent_date = self.invoice_model.search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice
        self.last_year_recent_date = date(
            self.recent_date.year - 1, self.recent_date.month,
            self.recent_date.day)

        self.account_tax_22 = self.tax_model.create({
            'name': '22%',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': self.received_vat_account,
            'type_tax_use': 'sale',
            })
        self.account_tax_22_credit = self.tax_model.create({
            'name': '22% credit',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': self.paid_vat_account,
            'type_tax_use': 'purchase',
            })

        self.vat_authority = self.account_model.create({
            'code': 'VAT AUTH',
            'name': 'VAT Authority',
            'reconcile': True,
            'user_type_id': self.env.ref(
                'account.data_account_type_payable').id,
            })

        self.account_payment_term = self.term_model.create({
            'name': '16 Days End of Month',
            'note': '16 Days End of Month',
            })
        self.term_line_model.create({
            'value': 'balance',
            'days': 16,
            'option': 'after_invoice_month',
            'payment_id': self.account_payment_term.id,
            })
        self.sale_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.purchase_journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]
        self.general_journal = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]

    def test_vat_statement(self):
        out_invoice_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_receivable').id
            )
        ], limit=1).id
        in_invoice_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_payable').id
            )
        ], limit=1).id
        out_invoice_line_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_expenses').id)
        ], limit=1).id
        in_invoice_line_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id)
        ], limit=1).id

        out_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': out_invoice_account,
            'journal_id': self.sale_journal.id,
            'partner_id': self.env.ref('base.res_partner_3').id,
            'type': 'out_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': out_invoice.id,
            'account_id': out_invoice_line_account,
            'name': 'service',
            'price_unit': 100,
            'quantity': 1,
            'invoice_line_tax_ids': [(6, 0, [self.account_tax_22.id])],
            })
        out_invoice.compute_taxes()
        out_invoice.action_invoice_open()

        in_invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'account_id': in_invoice_account,
            'journal_id': self.purchase_journal.id,
            'partner_id': self.env.ref('base.res_partner_4').id,
            'type': 'in_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': in_invoice.id,
            'account_id': in_invoice_line_account,
            'name': 'service',
            'price_unit': 50,
            'quantity': 1,
            'invoice_line_tax_ids': [(6, 0, [self.account_tax_22_credit.id])],
            })
        in_invoice.compute_taxes()
        in_invoice.action_invoice_open()

        last_year_in_invoice = self.invoice_model.create({
            'date_invoice': self.last_year_recent_date,
            'account_id': in_invoice_account,
            'journal_id': self.purchase_journal.id,
            'partner_id': self.env.ref('base.res_partner_4').id,
            'type': 'in_invoice',
            })
        self.invoice_line_model.create({
            'invoice_id': last_year_in_invoice.id,
            'account_id': in_invoice_line_account,
            'name': 'service',
            'price_unit': 50,
            'quantity': 1,
            'invoice_line_tax_ids': [(6, 0, [self.account_tax_22_credit.id])],
            })
        last_year_in_invoice.compute_taxes()
        last_year_in_invoice.action_invoice_open()

        self.last_year_vat_statement = self.vat_statement_model.create({
            'journal_id': self.general_journal.id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            'date': self.last_year_date,
            })
        self.last_year_period.vat_statement_id = self.last_year_vat_statement
        self.last_year_vat_statement.compute_amounts()

        self.vat_statement = self.vat_statement_model.create({
            'journal_id': self.general_journal.id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            })
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()
        self.vat_statement.previous_credit_vat_account_id = (
            self.received_vat_account)

        self.assertEqual(self.vat_statement.previous_credit_vat_amount, 11)
        self.assertTrue(self.vat_statement.previous_year_credit)
        self.assertEqual(self.vat_statement.authority_vat_amount, 0)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 11)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(
            len(self.vat_statement.debit_vat_account_line_ids), 1)
        self.assertEqual(
            len(self.vat_statement.credit_vat_account_line_ids), 1)
        self.vat_statement.advance_account_id = self.paid_vat_account
        self.vat_statement.advance_amount = 100
        self.vat_statement.refresh()
        self.assertEqual(self.vat_statement.authority_vat_amount, -100)
        self.vat_statement.create_move()
        self.assertEqual(self.vat_statement.state, 'confirmed')
        self.assertTrue(self.vat_statement.move_id)
        self.assertEqual(self.vat_statement.move_id.amount, 122)
        # TODO payment
