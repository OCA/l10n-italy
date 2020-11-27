#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from dateutil.rrule import MONTHLY
from odoo.addons.account.tests.account_test_users import AccountTestUsers


class TestTaxSP(AccountTestUsers):

    def setUp(self):
        super().setUp()
        self.tax_model = self.env['account.tax']
        self.invoice_model = self.env['account.invoice']
        self.term_model = self.env['account.payment.term']
        self.fp_model = self.env['account.fiscal.position']
        self.account_model = self.env['account.account']
        self.term_line_model = self.env['account.payment.term.line']
        self.invoice_line_model = self.env['account.invoice.line']
        self.vat_statement_model = self.env['account.vat.period.end.statement']
        account_user_type = self.env.ref('account.data_account_type_receivable')
        today = datetime.now().date()

        self.range_type = self.env['date.range.type'].create(
            {'name': 'Month',
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
        self.current_period = self.env['date.range'].search([
            ('date_start', '<=', today),
            ('date_end', '>=', today)
        ])

        paid_vat_account = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref(
                    'account.data_account_type_current_assets').id
            )
        ], limit=1).id
        received_vat_account = self.env['account.account'].search([
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

        self.account_tax_22sp = self.tax_model.create({
            'name': '22% SP',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': received_vat_account,
            'type_tax_use': 'sale',
            })

        self.account_tax_22 = self.tax_model.create({
            'name': '22%',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': received_vat_account,
            'type_tax_use': 'sale',
            })
        self.account_tax_22_credit = self.tax_model.create({
            'name': '22% credit',
            'amount': 22,
            'amount_type': 'percent',
            'vat_statement_account_id': paid_vat_account,
            'type_tax_use': 'purchase',
            })

        self.sp_fp = self.fp_model.create({
            'name': 'Split payment',
            'split_payment': True,
            'tax_ids': [(0, 0, {
                'tax_src_id': self.account_tax_22.id,
                'tax_dest_id': self.account_tax_22sp.id
            })]
            })
        self.company = self.env.ref('base.main_company')
        self.company.sp_account_id = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id
            )
        ], limit=1)
        self.a_recv = self.account_model.sudo(self.account_manager.id).create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=account_user_type.id,
                reconcile=True,
            ))
        self.a_sale = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id)
        ], limit=1)
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
        self.term_15_30 = self.term_model.create({
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
        # Set invoice date to recent date in the system
        # This solves problems with account_invoice_sequential_dates
        self.recent_date = self.invoice_model.search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice

        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.sales_journal.update_posted = True
        self.purchase_journal = self.env['account.journal'].search(
            [('type', '=', 'purchase')])[0]
        self.general_journal = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]

    def test_invoice(self):
        invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'partner_id': self.env.ref('base.res_partner_3').id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'fiscal_position_id': self.sp_fp.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'service',
                'account_id': self.a_sale.id,
                'quantity': 1,
                'price_unit': 100,
                'invoice_line_tax_ids': [(6, 0, {
                    self.account_tax_22sp.id
                    })]
                })]
            })
        invoice.compute_taxes()
        invoice.action_invoice_open()

        self.vat_statement = self.vat_statement_model.create({
            'journal_id': self.general_journal.id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            })
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()

        self.assertEqual(self.vat_statement.authority_vat_amount, 0)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 0)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(self.vat_statement.generic_vat_account_line_ids.amount,
                         22.0)

    def test_account_sp_company(self):
        account_user_type = self.env.ref(
            'account.data_account_type_receivable'
        )
        account_sp = self.account_model.sudo(self.account_manager.id).create(
            dict(
                code="split_payment_acc",
                name="Split payment account",
                user_type_id=account_user_type.id,
                reconcile=True,
            ))
        self.company.sp_account_id = account_sp.id

        invoice = self.invoice_model.create({
            'date_invoice': self.recent_date,
            'partner_id': self.env.ref('base.res_partner_3').id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'fiscal_position_id': self.sp_fp.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'service',
                'account_id': self.a_sale.id,
                'quantity': 1,
                'price_unit': 100,
                'invoice_line_tax_ids': [(6, 0, {
                    self.account_tax_22sp.id
                    })]
                })]
            })
        invoice.compute_taxes()
        invoice.action_invoice_open()

        self.vat_statement = self.vat_statement_model.create({
            'journal_id': self.general_journal.id,
            'authority_vat_account_id': self.vat_authority.id,
            'payment_term_id': self.account_payment_term.id,
            })
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()
        self.assertEqual(
            self.vat_statement.generic_vat_account_line_ids.account_id.id,
            account_sp.id
        )
