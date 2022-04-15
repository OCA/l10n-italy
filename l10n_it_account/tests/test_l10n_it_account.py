import datetime

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccount(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.data_account_type_current_assets = cls.env.ref(
            "account.data_account_type_current_assets"
        )
        cls.data_account_type_current_liabilities = cls.env.ref(
            "account.data_account_type_current_liabilities"
        )
        cls.group_1 = cls.env["account.group"].create(
            {
                "name": "1",
                "code_prefix_start": "it_account_",
            }
        )
        cls.iva_22I5 = cls.env["account.tax"].create(
            {
                "name": "IVA al 22% detraibile al 50%",
                "description": "22I5",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include": False,
                "invoice_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (5, 0, 0),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 50,
                            "repartition_type": "tax",
                            "account_id": cls.company_data["default_account_assets"].id,
                        },
                    ),
                ],
            }
        )
        cls.vat_not_deductible = cls.env["account.tax"].create(
            {
                "name": "VAT 22% not deductible",
                "description": "NOTDED",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "price_include": False,
                "invoice_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                        },
                    ),
                ],
            }
        )

    def test_group_constraint(self):
        self.env["account.account"].create(
            {
                "name": "it_account_1",
                "code": "it_account_1",
                "user_type_id": self.data_account_type_current_assets.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["account.account"].create(
                {
                    "name": "it_account_2",
                    "code": "it_account_2",
                    "user_type_id": self.data_account_type_current_liabilities.id,
                }
            )

    def test_vat_22_50(self):
        today = fields.Date.today()
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="in_invoice")
        )
        move_form.partner_id = self.env.ref("base.res_partner_12")
        move_form.invoice_date = today
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "test line"
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.iva_22I5)
        rslt = move_form.save()
        rslt.action_post()
        context = {
            "from_date": today,
            "to_date": today,
        }
        tax = self.env["account.tax"].with_context(context).browse(self.iva_22I5.id)
        self.assertEqual(tax.balance, -22)
        self.assertEqual(tax.deductible_balance, -11)
        self.assertEqual(tax.undeductible_balance, -11)

    def test_vat_22_not_deductible(self):
        today = fields.Date.today()
        self.init_invoice(
            "in_invoice",
            invoice_date=today,
            amounts=[100],
            taxes=self.vat_not_deductible,
            post=True,
        )
        context = {
            "from_date": today,
            "to_date": today,
        }
        tax = (
            self.env["account.tax"]
            .with_context(context)
            .browse(self.vat_not_deductible.id)
        )
        self.assertEqual(tax.balance, -22)
        self.assertEqual(tax.deductible_balance, 0)
        self.assertEqual(tax.undeductible_balance, -22)

    def test_partially_deductible_balance_recomputation(self):
        """Check that deductible and not deductible balances
        are computed correctly for different dates."""
        today = fields.Date.today()
        self.init_invoice(
            "in_invoice",
            partner=self.env.ref("base.res_partner_12"),
            invoice_date=today,
            post=True,
            amounts=[100],
            taxes=self.iva_22I5,
        )
        tomorrow = today + datetime.timedelta(days=1)
        self.init_invoice(
            "in_invoice",
            partner=self.env.ref("base.res_partner_12"),
            invoice_date=tomorrow,
            post=True,
            amounts=[200],
            taxes=self.iva_22I5,
        )

        # Check today's balance
        self.check_date_balance(self.iva_22I5, today, -11, -11)

        # Check tomorrow's balance
        self.check_date_balance(self.iva_22I5, tomorrow, -22, -22)

    def check_date_balance(self, tax, date, deductible, not_deductible):
        """Compare expected balances with tax's balance in specified date."""
        tax = tax.with_context(
            from_date=date,
            to_date=date,
        )
        self.assertEqual(tax.deductible_balance, deductible)
        self.assertEqual(tax.undeductible_balance, not_deductible)
