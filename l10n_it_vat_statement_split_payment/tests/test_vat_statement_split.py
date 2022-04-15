#  Copyright 2015 Agile Business Group <http://www.agilebg.com>
#  Copyright 2021 Lorenzo Battistini @ TAKOBI
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from dateutil.rrule import MONTHLY

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestTaxSP(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.tax_model = cls.env["account.tax"]
        cls.move_model = cls.env["account.move"]
        cls.term_model = cls.env["account.payment.term"]
        cls.fp_model = cls.env["account.fiscal.position"]
        cls.account_model = cls.env["account.account"]
        cls.term_line_model = cls.env["account.payment.term.line"]
        cls.vat_statement_model = cls.env["account.vat.period.end.statement"]
        account_user_type = cls.env.ref("account.data_account_type_receivable")
        today = datetime.now().date()

        cls.range_type = cls.env["date.range.type"].create(
            {"name": "Month", "company_id": False, "allow_overlap": False}
        )
        generator = cls.env["date.range.generator"]
        generator = generator.create(
            {
                "date_start": "%s-01-01" % datetime.now().year,
                "name_prefix": "%s-" % datetime.now().year,
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        )
        generator.action_apply()
        cls.current_period = cls.env["date.range"].search(
            [("date_start", "<=", today), ("date_end", ">=", today)]
        )

        paid_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        cls.env.ref("account.data_account_type_current_assets").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        received_vat_account = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        cls.env.ref("account.data_account_type_current_liabilities").id,
                    )
                ],
                limit=1,
            )
            .id
        )

        # ----- Set invoice date to recent date in the system
        # ----- This solves problems with account_invoice_sequential_dates
        cls.recent_date = cls.move_model.search(
            [("invoice_date", "!=", False)], order="invoice_date desc", limit=1
        ).invoice_date

        cls.account_tax_22sp = cls.company_data["default_tax_sale"].copy(
            {
                "name": "22% SP",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": received_vat_account,
                "type_tax_use": "sale",
            }
        )

        cls.account_tax_22 = cls.company_data["default_tax_sale"].copy(
            {
                "name": "22%",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": received_vat_account,
                "type_tax_use": "sale",
            }
        )
        cls.account_tax_22_credit = cls.company_data["default_tax_purchase"].copy(
            {
                "name": "22% credit",
                "amount": 22,
                "amount_type": "percent",
                "vat_statement_account_id": paid_vat_account,
                "type_tax_use": "purchase",
            }
        )

        cls.sp_fp = cls.fp_model.create(
            {
                "name": "Split payment",
                "split_payment": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": cls.account_tax_22.id,
                            "tax_dest_id": cls.account_tax_22sp.id,
                        },
                    )
                ],
            }
        )
        cls.company = cls.company_data["company"]
        cls.company.sp_account_id = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_current_assets").id,
                )
            ],
            limit=1,
        )
        cls.a_recv = cls.account_model.create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=account_user_type.id,
                reconcile=True,
            )
        )
        cls.a_sale = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        cls.vat_authority = cls.account_model.create(
            {
                "code": "VAT AUTH",
                "name": "VAT Authority",
                "reconcile": True,
                "user_type_id": cls.env.ref("account.data_account_type_payable").id,
            }
        )

        cls.account_payment_term = cls.term_model.create(
            {
                "name": "16 Days End of Month",
                "note": "16 Days End of Month",
            }
        )
        cls.term_line_model.create(
            {
                "value": "balance",
                "days": 16,
                "option": "after_invoice_month",
                "payment_id": cls.account_payment_term.id,
            }
        )
        cls.term_15_30 = cls.term_model.create(
            {
                "name": "15 30",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "value": "percent",
                            "value_amount": 50,
                            "days": 15,
                            "sequence": 1,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "value": "balance",
                            "days": 30,
                            "sequence": 2,
                        },
                    ),
                ],
            }
        )
        # Set invoice date to recent date in the system
        # This solves problems with account_invoice_sequential_dates
        cls.recent_date = cls.move_model.search(
            [("invoice_date", "!=", False)], order="invoice_date desc", limit=1
        ).invoice_date

        cls.sales_journal = cls.company_data["default_journal_sale"]
        cls.general_journal = cls.company_data["default_journal_misc"]

    def test_invoice(self):
        invoice = self.move_model.with_context(default_move_type="out_invoice").create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "journal_id": self.sales_journal.id,
                "fiscal_position_id": self.sp_fp.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": self.a_sale.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, {self.account_tax_22sp.id})],
                        },
                    )
                ],
            }
        )
        invoice.action_post()

        self.vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
            }
        )
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()

        self.assertEqual(self.vat_statement.authority_vat_amount, 0)
        self.assertEqual(self.vat_statement.deductible_vat_amount, 0)
        self.assertEqual(self.vat_statement.residual, 0)
        self.assertEqual(self.vat_statement.generic_vat_account_line_ids.amount, 22.0)

    def test_account_sp_company(self):
        account_user_type = self.env.ref("account.data_account_type_receivable")
        account_sp = self.account_model.create(
            dict(
                code="split_payment_acc",
                name="Split payment account",
                user_type_id=account_user_type.id,
                reconcile=True,
            )
        )
        self.company.sp_account_id = account_sp.id

        invoice = self.move_model.with_context(default_move_type="out_invoice").create(
            {
                "invoice_date": self.recent_date,
                "partner_id": self.env.ref("base.res_partner_3").id,
                "journal_id": self.sales_journal.id,
                "fiscal_position_id": self.sp_fp.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "service",
                            "account_id": self.a_sale.id,
                            "quantity": 1,
                            "price_unit": 100,
                            "tax_ids": [(6, 0, {self.account_tax_22sp.id})],
                        },
                    )
                ],
            }
        )
        invoice.action_post()

        self.vat_statement = self.vat_statement_model.create(
            {
                "journal_id": self.general_journal.id,
                "authority_vat_account_id": self.vat_authority.id,
                "payment_term_id": self.account_payment_term.id,
            }
        )
        self.current_period.vat_statement_id = self.vat_statement
        self.vat_statement.compute_amounts()
        self.assertEqual(
            self.vat_statement.generic_vat_account_line_ids.account_id.id, account_sp.id
        )
