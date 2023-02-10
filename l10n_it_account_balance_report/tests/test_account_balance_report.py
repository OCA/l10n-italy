# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo.tests.common import Form, TransactionCase

DEFAULT_FACTUR_ITALIAN_DATE_FORMAT = "%Y-%m-%d"


class AccountBalanceReport(TransactionCase):
    def setUp(self):
        super().setUp()

        # Date

        self.date = datetime.strptime(
            "2022-03-24", DEFAULT_FACTUR_ITALIAN_DATE_FORMAT
        ).strftime(DEFAULT_FACTUR_ITALIAN_DATE_FORMAT)

        # Wizard trial balance report Object

        self.wizard_trial_balance_report_obj = self.env["trial.balance.report.wizard"]

        # Account balance report Object

        self.account_balance_report_obj = self.env["account_balance_report"]

        # Partners

        self.customer = self.env["res.partner"].search(
            [("customer_rank", ">", 0)], limit=1
        )
        self.vendor = self.env["res.partner"].search(
            [("supplier_rank", ">", 0)], limit=1
        )

        # Account user types

        self.account_account_type_current_liabilities = self.env.ref(
            "account.data_account_type_current_liabilities"
        )

        self.account_account_type_expense = self.env.ref(
            "account.data_account_type_expenses"
        )

        # Accounts

        account_account = self.env["account.account"]

        self.account_251000 = account_account.search(
            [("code", "=", "251000"), ("company_id", "=", self.env.company.id)]
        )

        self.account_131000 = account_account.search(
            [("code", "=", "131000"), ("company_id", "=", self.env.company.id)]
        )

        with Form(account_account) as account_form:
            account_form.name = "debiti per ritenute da versare"
            account_form.code = "260200"
            account_form.user_type_id = self.account_account_type_current_liabilities

        self.account_260200 = account_form.save()

        with Form(account_account) as account_form:
            account_form.name = "personale c/retribuzioni"
            account_form.code = "262000"
            account_form.user_type_id = self.account_account_type_current_liabilities

        self.account_262000 = account_form.save()

        with Form(account_account) as account_form:
            account_form.name = "debiti v/istituti previdenziali"
            account_form.code = "263000"
            account_form.user_type_id = self.account_account_type_current_liabilities

        self.account_263000 = account_form.save()

        with Form(account_account) as account_form:
            account_form.name = "salari e stipendi"
            account_form.code = "440100"
            account_form.user_type_id = self.account_account_type_expense

        self.account_440100 = account_form.save()

        with Form(account_account) as account_form:
            account_form.name = "oneri sociali"
            account_form.code = "440200"
            account_form.user_type_id = self.account_account_type_expense

        self.account_440200 = account_form.save()

        # Taxes

        taxes_obj = self.env["account.tax"].with_context(
            default_company_id=self.env.company.id,
        )

        with Form(taxes_obj) as tax_form:
            tax_form.name = "IVA 22% Sale"
            tax_form.amount = 22.0
            tax_form.type_tax_use = "sale"

        self.tax_22_s = tax_form.save()

        (
            self.tax_22_s.invoice_repartition_line_ids.filtered(
                lambda invoice_repartition_line_id: invoice_repartition_line_id.repartition_type
                == "tax"
            )
            + self.tax_22_s.refund_repartition_line_ids.filtered(
                lambda invoice_repartition_line_id: invoice_repartition_line_id.repartition_type
                == "tax"
            )
        ).write({"account_id": self.account_251000.id})

        with Form(taxes_obj) as tax_form:
            tax_form.name = "IVA 22% Purchase"
            tax_form.amount = 22.0
            tax_form.type_tax_use = "purchase"

        self.tax_22_p = tax_form.save()

        (
            self.tax_22_p.invoice_repartition_line_ids.filtered(
                lambda invoice_repartition_line_id: invoice_repartition_line_id.repartition_type
                == "tax"
            )
            + self.tax_22_p.refund_repartition_line_ids.filtered(
                lambda invoice_repartition_line_id: invoice_repartition_line_id.repartition_type
                == "tax"
            )
        ).write({"account_id": self.account_131000.id})

        # Invoices

        invoices_obj = self.env["account.move"]

        # Customer invoices
        with Form(
            invoices_obj.with_context(
                account_predictive_bills_disable_prediction=True,
                default_move_type="out_invoice",
                default_company_id=self.env.company.id,
            )
        ) as invoice_form:
            invoice_form.partner_id = self.customer
            invoice_form.invoice_date = self.date

            with invoice_form.invoice_line_ids.new() as invoice_line_form:
                invoice_line_form.name = "Sandwich"
                invoice_line_form.quantity = 1
                invoice_line_form.price_unit = 1000.0
                invoice_line_form.tax_ids.clear()
                invoice_line_form.tax_ids.add(self.tax_22_s)

        self.customer_invoice = invoice_form.save()

        self.customer_invoice.action_post()

        # Vendors Invoices

        with Form(
            invoices_obj.with_context(
                account_predictive_bills_disable_prediction=True,
                default_move_type="in_invoice",
                default_company_id=self.env.company.id,
            )
        ) as invoice_form:
            invoice_form.partner_id = self.vendor
            invoice_form.invoice_date = self.date

            with invoice_form.invoice_line_ids.new() as invoice_line_form:
                invoice_line_form.name = "Sandwich"
                invoice_line_form.quantity = 1
                invoice_line_form.price_unit = 700.0
                invoice_line_form.tax_ids.clear()
                invoice_line_form.tax_ids.add(self.tax_22_p)

        self.vendor_invoice = invoice_form.save()

        self.vendor_invoice.action_post()

        # Entries

        with Form(
            invoices_obj.with_context(
                account_predictive_bills_disable_prediction=True,
                default_move_type="entry",
                default_company_id=self.env.company.id,
            )
        ) as invoice_form:
            invoice_form.date = self.date

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_263000
                invoice_line_form.credit = 200.0

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_440200
                invoice_line_form.debit = 200.0

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_260200
                invoice_line_form.credit = 250.0

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_263000
                invoice_line_form.credit = 250.0

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_440100
                invoice_line_form.debit = 1500.0

            with invoice_form.line_ids.new() as invoice_line_form:
                invoice_line_form.account_id = self.account_262000
                invoice_line_form.credit = 1000.0

        self.entry = invoice_form.save()

        self.entry.action_post()

        # Payment Vendor Invoices

        with Form(
            self.env["account.payment.register"].with_context(
                active_model="account.move",
                active_ids=self.vendor_invoice.ids,
            )
        ) as account_payment_register_form:
            account_payment_register_form.payment_date = self.date
            account_payment_register_form.amount = 500.0

        self.account_payment_register = account_payment_register_form.save()

        self.account_payment_register.action_create_payments()

        # Date Range
        date_range_type = self.env["date.range.type"]

        self.date_range_type = date_range_type.search([])

        if not self.date_range_type:

            with Form(date_range_type) as date_range_type_form:
                date_range_type_form.name = "Fiscal Year"

            self.date_range_type = date_range_type_form.save()

        with Form(self.env["date.range"]) as date_range_form:
            date_range_form.name = "2022"
            date_range_form.type_id = self.date_range_type
            date_range_form.date_start = datetime.strptime(
                "2022-01-01", DEFAULT_FACTUR_ITALIAN_DATE_FORMAT
            ).strftime(DEFAULT_FACTUR_ITALIAN_DATE_FORMAT)
            date_range_form.date_end = datetime.strptime(
                "2022-12-31", DEFAULT_FACTUR_ITALIAN_DATE_FORMAT
            ).strftime(DEFAULT_FACTUR_ITALIAN_DATE_FORMAT)

        self.date_range = date_range_form.save()

    def check_balance_sheet(self, result):
        account_balance_report = self.account_balance_report_obj.browse(
            result["context"]["report_action"]["context"]["active_ids"][0]
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "211000"
            ).balance,
            -354.0,
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "251000"
            ).balance,
            -220.0,
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "260200"
            ).balance,
            -250.0,
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "262000"
            ).balance,
            -1000.0,
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "263000"
            ).balance,
            -450.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "101404"
            ).balance,
            -500.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "121000"
            ).balance,
            1220.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "131000"
            ).balance,
            154.0,
        )

    def test_balance_sheet(self):
        with Form(
            self.wizard_trial_balance_report_obj.with_context(
                default_account_balance_report_type="balance_sheet"
            )
        ) as wizard_trial_balance_report_form:
            wizard_trial_balance_report_form.date_range_id = self.date_range

        self.wizard_trial_balance_report = wizard_trial_balance_report_form.save()

        result = self.wizard_trial_balance_report.button_export_html()

        self.check_balance_sheet(result)

        result = self.wizard_trial_balance_report.button_export_pdf()

        self.check_balance_sheet(result)

        result = self.wizard_trial_balance_report.button_export_xlsx()

        self.check_balance_sheet(result)

    def check_profit_and_loss(self, result):
        account_balance_report = self.account_balance_report_obj.browse(
            result["context"]["report_action"]["context"]["active_ids"][0]
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "400000"
            ).balance,
            -1000.0,
        )

        self.assertEqual(
            account_balance_report.section_credit_ids.filtered(
                lambda section_credit: section_credit.code == "999999"
            ).balance,
            0.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "440100"
            ).balance,
            1500.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "440200"
            ).balance,
            200.0,
        )

        self.assertEqual(
            account_balance_report.section_debit_ids.filtered(
                lambda section_debit: section_debit.code == "600000"
            ).balance,
            700.0,
        )

    def test_profit_and_loss(self):
        with Form(
            self.wizard_trial_balance_report_obj.with_context(
                default_account_balance_report_type="profit_loss"
            )
        ) as wizard_trial_balance_report_form:
            wizard_trial_balance_report_form.date_range_id = self.date_range

        self.wizard_trial_balance_report = wizard_trial_balance_report_form.save()

        result = self.wizard_trial_balance_report.button_export_html()

        self.check_profit_and_loss(result)

        result = self.wizard_trial_balance_report.button_export_pdf()

        self.check_profit_and_loss(result)

        result = self.wizard_trial_balance_report.button_export_xlsx()

        self.check_profit_and_loss(result)
