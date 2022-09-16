#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.tests.common import TransactionCase, Form
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

    def _create_vendor_bill(self, partner, date_invoice, price_unit, tax):
        """
        Create an open Vendor Bill for `partner` having date `date_invoice`.
        The Bill will also have a Line having Price `price_unit` and Tax `tax`.
        """
        bill_model = self.invoice_model.with_context(
            type='in_invoice',
        )
        bill_form = Form(bill_model)
        bill_form.partner_id = partner
        bill_form.date_invoice = date_invoice
        with bill_form.invoice_line_ids.new() as line:
            line.invoice_line_tax_ids.clear()
            line.invoice_line_tax_ids.add(tax)
            line.name = "Test Invoice Line"
            line.price_unit = price_unit
        bill = bill_form.save()
        bill.action_invoice_open()
        return bill

    def _get_statement(self, period, statement_date, accounts):
        """
        Create a VAT Statement in date `statement_date`
        for Period `period` and Accounts `accounts`.
        """
        # Create statement
        statement_form = Form(self.vat_statement_model)
        statement_form.journal_id = self.general_journal
        statement_form.authority_vat_account_id = self.vat_authority
        statement_form.payment_term_id = self.account_payment_term
        statement_form.date = statement_date
        statement_form.account_ids.clear()
        for account in accounts:
            statement_form.account_ids.add(account)
        statement = statement_form.save()

        # Add period
        add_period_model = self.env['add.period.to.vat.statement']
        add_period_model = add_period_model \
            .with_context(
                active_id=statement.id,
                active_model=statement._name,
            )
        add_period_form = Form(add_period_model)
        add_period_form.period_id = period
        add_period = add_period_form.save()
        add_period.add_period()
        return statement

    def test_different_previous_vat_statements(self):
        """
        Statements for different Accounts
        only count previous Amounts from Statements with the same Accounts.
        """
        # Arrange: Create two different VAT Statements
        # selecting two different Accounts
        partner = self.env.ref('base.res_partner_4')
        tax = self.account_tax_22_credit
        tax_statement_account = tax.vat_statement_account_id
        last_year_bill = self._create_vendor_bill(
            partner, self.last_year_recent_date,
            10, tax,
        )
        self.assertEqual(last_year_bill.state, 'open')
        last_year_period = self.last_year_period
        last_year_statement = self._get_statement(
            last_year_period,
            self.last_year_date,
            tax_statement_account,
        )
        self.assertTrue(last_year_statement)

        # Create another Bill and Statement
        other_tax_statement_account = tax_statement_account.copy()
        other_tax = tax.copy(
            default={
                'vat_statement_account_id': other_tax_statement_account.id,
            },
        )
        other_last_year_bill = self._create_vendor_bill(
            partner, self.last_year_recent_date,
            20, other_tax,
        )
        self.assertEqual(other_last_year_bill.state, 'open')
        last_year_period.type_id.allow_overlap = True
        other_last_year_period = last_year_period.copy(
            default={
                'name': "Test Other last Year Period",
                'vat_statement_id': False,
            },
        )
        other_last_year_statement = self._get_statement(
            other_last_year_period,
            self.last_year_date,
            other_tax_statement_account,
        )
        self.assertTrue(other_last_year_statement)

        # Act: Create this Year's Statements,
        # one for each Account used in previous Statements
        today = fields.Date.today()
        current_period = self.current_period
        statement = self._get_statement(
            current_period,
            today,
            tax_statement_account,
        )

        current_period.type_id.allow_overlap = True
        other_current_period = current_period.copy(
            default={
                'name': "Test Other current Period",
                'vat_statement_id': False,
            },
        )
        other_statement = self._get_statement(
            other_current_period,
            today,
            other_tax_statement_account,
        )

        # Assert: Each one of this Year's Statements counts as previous Amount
        # only the corresponding last Year's Statement
        self.assertEqual(
            statement.previous_credit_vat_amount,
            -last_year_statement.authority_vat_amount,
        )
        self.assertEqual(
            other_statement.previous_credit_vat_amount,
            -other_last_year_statement.authority_vat_amount,
        )
