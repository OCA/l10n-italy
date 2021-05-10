from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase


class TestAccount(TransactionCase):
    def setUp(self):
        super(TestAccount, self).setUp()
        self.data_account_type_current_assets = self.env.ref(
            "account.data_account_type_current_assets"
        )
        self.data_account_type_current_liabilities = self.env.ref(
            "account.data_account_type_current_liabilities"
        )
        self.group_1 = self.env["account.group"].create(
            {
                "name": "1",
                "code_prefix_start": "it_account_",
            }
        )
        self.iva_22I5 = self.env["account.tax"].create(
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
                            "account_id": self.env.ref(
                                "l10n_generic_coa.1_tax_paid"
                            ).id,
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
                            "account_id": self.env.ref(
                                "l10n_generic_coa.1_tax_paid"
                            ).id,
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
