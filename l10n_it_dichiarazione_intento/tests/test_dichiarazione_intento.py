# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import Form, SavepointCase
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TestDichiarazioneIntento(SavepointCase):
    def _create_dichiarazione(self, partner, type_d):
        return self.env["dichiarazione.intento"].create(
            {
                "partner_id": partner.id,
                "partner_document_number": "PartnerTest%s" % partner.id,
                "partner_document_date": self.today_date,
                "date": self.today_date,
                "date_start": self.today_date,
                "date_end": self.today_date,
                "taxes_ids": [(6, 0, [self.tax1.id])],
                "limit_amount": 1000.00,
                "fiscal_position_id": self.fiscal_position.id,
                "type": type_d,
                "telematic_protocol": "08060120341234567-000001",
            }
        )

    def _create_invoice(self, name, partner, tax=False, date=False, in_type=False):
        invoice_form = Form(
            self.env["account.move"].with_context(
                default_move_type="in_invoice" if in_type else "out_invoice"
            )
        )
        invoice_form.partner_id = partner
        invoice_form.invoice_date = date if date else self.today_date
        invoice_form.name = "Test invoice " + name
        invoice_form.invoice_payment_term_id = self.env.ref(
            "account.account_payment_term_advance"
        )

        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = self.env.ref("product.product_product_5")
            invoice_line.quantity = 10.00
            invoice_line.account_id = self.a_cost if in_type else self.a_sale
            invoice_line.name = "test line"
            invoice_line.price_unit = 90.00
            if tax:
                invoice_line.tax_ids.clear()
                invoice_line.tax_ids.add(tax)

        invoice = invoice_form.save()
        return invoice

    def _create_refund(self, partner, tax=False, date=False, invoice=False):
        refund_form = Form(
            self.env["account.move"].with_context(default_move_type="out_refund")
        )
        refund_form.partner_id = partner
        refund_form.name = "Test Refund for Dichiarazione"
        refund_form.invoice_date = date if date else self.today_date
        refund_form.invoice_payment_term_id = self.env.ref(
            "account.account_payment_term_advance"
        )

        with refund_form.invoice_line_ids.new() as refund_line:
            refund_line.quantity = 1.00
            refund_line.account_id = self.a_sale
            refund_line.name = "test refund line"
            refund_line.price_unit = 100.00
            if tax:
                refund_line.tax_ids.clear()
                refund_line.tax_ids.add(tax)

        refund = refund_form.save()
        return refund

    def setUp(self):

        super(TestDichiarazioneIntento, self).setUp()
        self.tax_model = self.env["account.tax"]
        self.a_sale = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        self.a_cost = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_direct_costs").id,
                )
            ],
            limit=1,
        )
        self.today_date = fields.Date.today()
        self.partner1 = self.env.ref("base.res_partner_2")
        self.partner2 = self.env.ref("base.res_partner_12")
        self.partner3 = self.env.ref("base.res_partner_10")
        self.partner4 = self.env.ref("base.res_partner_4")
        self.tax22 = self.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
            }
        )
        self.tax10 = self.tax_model.create(
            {
                "name": "10%",
                "amount": 10,
            }
        )
        self.tax2 = self.tax_model.create(
            {
                "name": "2%",
                "amount": 2,
            }
        )
        self.tax1 = self.tax_model.create(
            {
                "name": "FC INC",
                "amount": 0,
                "price_include": True,
            }
        )
        self.fiscal_position = self.env["account.fiscal.position"].create(
            {
                "name": "Dichiarazione Test",
                "valid_for_dichiarazione_intento": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": self.tax10.id,
                            "tax_dest_id": self.tax1.id,
                        },
                    )
                ],
            }
        )
        self.fiscal_position_with_wrong_taxes = self.env[
            "account.fiscal.position"
        ].create(
            {
                "name": "Dichiarazione Test Wrong",
                "valid_for_dichiarazione_intento": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": self.tax10.id,
                            "tax_dest_id": self.tax22.id,
                        },
                    )
                ],
            }
        )
        self.fiscal_position2 = self.env["account.fiscal.position"].create(
            {
                "name": "Dichiarazione Test 2",
                "valid_for_dichiarazione_intento": False,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": self.tax22.id,
                            "tax_dest_id": self.tax10.id,
                        },
                    )
                ],
            }
        )

        self.dichiarazione1 = self._create_dichiarazione(self.partner1, "out")
        self.dichiarazione2 = self._create_dichiarazione(self.partner2, "out")
        self.dichiarazione3 = self._create_dichiarazione(self.partner2, "out")
        self.env["dichiarazione.intento.yearly.limit"].create(
            {
                "year": self.today_date.year,
                "limit_amount": 50000.0,
                "company_id": self.env.company.id,
            }
        )
        self.dichiarazione4 = self._create_dichiarazione(self.partner4, "in")
        self.invoice1 = self._create_invoice("1", self.partner1)
        self.invoice2 = self._create_invoice("2", self.partner1, tax=self.tax1)
        self.invoice3 = self._create_invoice("3", self.partner1, tax=self.tax1)
        self.invoice_without_valid_taxes = self._create_invoice(
            "no valid taxes", self.partner1, tax=self.tax2
        )
        future_date = datetime.today() + timedelta(days=10)
        future_date = future_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        self.invoice_future = self._create_invoice(
            "future", self.partner1, date=future_date, tax=self.tax1
        )
        self.refund1 = self._create_refund(
            self.partner1, tax=self.tax1, invoice=self.invoice2
        )
        self.invoice4 = self._create_invoice("4", self.partner3, tax=self.tax22)
        self.invoice4.fiscal_position_id = self.fiscal_position2.id
        self.invoice5 = self._create_invoice(
            "5", self.partner4, tax=self.tax1, in_type=True
        )

    def test_dichiarazione_data(self):
        self.assertTrue(self.dichiarazione1.number)

    def test_costraints(self):
        with self.assertRaises(ValidationError):
            self.dichiarazione1.fiscal_position_id = (
                self.fiscal_position_with_wrong_taxes.id
            )

    def test_get_valid(self):
        dichiarazione_model = self.env["dichiarazione.intento"]
        self.assertFalse(dichiarazione_model.get_valid())
        records = dichiarazione_model.get_valid(
            type_d="out", partner_id=self.partner1.id, date=self.today_date
        )
        self.assertEqual(len(records), 1)
        records = dichiarazione_model.get_valid(
            type_d="out", partner_id=self.partner2.id, date=self.today_date
        )
        self.assertEqual(len(records), 2)

    def test_dichiarazione_state_change(self):
        self.assertEqual(self.dichiarazione1.state, "valid")
        # ----- Close dichiarazione by moving end date before today
        previuos_date = datetime.today() - timedelta(days=10)
        self.dichiarazione1.date_start = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT
        )
        self.dichiarazione1.date_end = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT
        )
        self.assertEqual(self.dichiarazione1.state, "expired")

    def test_invoice_validation_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_post()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_future.action_post()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_without_valid_taxes.action_post()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_reopen_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_post()
        self.invoice1.button_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_under_dichiarazione_limit(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_post()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_over_dichiarazione_limit(self):
        self.invoice2.action_post()
        with self.assertRaises(UserError):
            self.invoice3.action_post()

    def test_invoice_reopen_with_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_post()
        self.invoice2.button_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_refund(self):
        self.invoice2.action_post()
        previous_used_amount = self.dichiarazione1.used_amount
        self.refund1.action_post()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_refund_with_amount_bigger_than_residual(self):
        self.invoice2.action_post()
        refund_form = Form(self.refund1)
        with refund_form.invoice_line_ids.edit(0) as line_form:
            line_form.quantity = 10
        refund_form.save()

        # Check that base amount has been updated
        self.assertEqual(self.refund1.amount_untaxed, 1000)

        # Refund goes over plafond: 100 + 1000 > 1000
        self.assertEqual(self.dichiarazione1.available_amount, 100)
        self.assertEqual(self.refund1.amount_untaxed, 1000)
        self.assertEqual(self.dichiarazione1.limit_amount, 1000)
        with self.assertRaises(UserError):
            self.refund1.action_post()

    def test_fiscal_position_no_dichiarazione(self):
        self.invoice4._onchange_date_invoice()
        self.assertEqual(self.invoice4.fiscal_position_id.id, self.fiscal_position2.id)

    def test_invoice_vendor_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione4.used_amount
        self.assertAlmostEqual(previous_used_amount, 0.0, 2)
        self.invoice5.action_post()
        post_used_amount = self.dichiarazione4.used_amount
        self.assertAlmostEqual(post_used_amount, 900.0, 2)
