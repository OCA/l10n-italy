# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import Form
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


class TestDeclarationOfIntent(AccountTestInvoicingCommon):
    @classmethod
    def _create_declaration(cls, partner, type_d):
        return cls.env["l10n_it_declaration_of_intent.declaration"].create(
            {
                "partner_id": partner.id,
                "partner_document_number": "PartnerTest%s" % partner.id,
                "partner_document_date": cls.today_date,
                "date": cls.today_date,
                "date_start": cls.today_date,
                "date_end": cls.today_date,
                "taxes_ids": [(6, 0, [cls.tax1.id])],
                "limit_amount": 1000.00,
                "fiscal_position_id": cls.fiscal_position.id,
                "type": type_d,
                "telematic_protocol": "08060120341234567-000001",
            }
        )

    @classmethod
    def _create_invoice(cls, name, partner, tax=False, date=False, in_type=False):
        invoice_form = Form(
            cls.env["account.move"].with_context(
                default_move_type="in_invoice" if in_type else "out_invoice"
            )
        )
        invoice_form.partner_id = partner
        invoice_form.invoice_date = date if date else cls.today_date
        invoice_form.name = "Test invoice " + name
        invoice_form.invoice_payment_term_id = cls.env.ref(
            "account.account_payment_term_advance"
        )

        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = cls.env.ref("product.product_product_5")
            invoice_line.quantity = 10.00
            invoice_line.account_id = cls.a_cost if in_type else cls.a_sale
            invoice_line.name = "test line"
            invoice_line.price_unit = 90.00
            if tax:
                invoice_line.tax_ids.clear()
                invoice_line.tax_ids.add(tax)

        invoice = invoice_form.save()
        return invoice

    @classmethod
    def _create_refund(cls, partner, tax=False, date=False, in_type=False):
        refund_form = Form(
            cls.env["account.move"].with_context(
                default_move_type="in_refund" if in_type else "out_refund"
            )
        )
        refund_form.partner_id = partner
        refund_form.name = "Test Refund for Declaration"
        refund_form.invoice_date = date if date else cls.today_date
        refund_form.invoice_payment_term_id = cls.env.ref(
            "account.account_payment_term_advance"
        )

        with refund_form.invoice_line_ids.new() as refund_line:
            refund_line.quantity = 1.00
            refund_line.account_id = cls.a_sale
            refund_line.name = "test refund line"
            refund_line.price_unit = 100.00
            if tax:
                refund_line.tax_ids.clear()
                refund_line.tax_ids.add(tax)

        refund = refund_form.save()
        return refund

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        # Copy declaration sequence to current company
        cls.env.ref("l10n_it_declaration_of_intent.declaration_of_intent_seq").copy(
            default=dict(
                company_id=cls.env.company.id,
            )
        )

        cls.tax_model = cls.env["account.tax"]
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
        cls.a_cost = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_direct_costs").id,
                )
            ],
            limit=1,
        )
        cls.today_date = fields.Date.today()
        cls.partner1 = cls.env.ref("base.res_partner_2")
        cls.partner2 = cls.env.ref("base.res_partner_12")
        cls.partner3 = cls.env.ref("base.res_partner_10")
        cls.partner4 = cls.env.ref("base.res_partner_4")
        cls.tax22 = cls.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
            }
        )
        cls.tax10 = cls.tax_model.create(
            {
                "name": "10%",
                "amount": 10,
            }
        )
        cls.tax2 = cls.tax_model.create(
            {
                "name": "2%",
                "amount": 2,
            }
        )
        cls.tax1 = cls.tax_model.create(
            {
                "name": "FC INC",
                "amount": 0,
                "price_include": True,
            }
        )
        cls.fiscal_position = cls.env["account.fiscal.position"].create(
            {
                "name": "Test declaration",
                "valid_for_declaration_of_intent": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": cls.tax10.id,
                            "tax_dest_id": cls.tax1.id,
                        },
                    )
                ],
            }
        )
        cls.fiscal_position_with_wrong_taxes = cls.env[
            "account.fiscal.position"
        ].create(
            {
                "name": "Test wrong declaration",
                "valid_for_declaration_of_intent": True,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": cls.tax10.id,
                            "tax_dest_id": cls.tax22.id,
                        },
                    )
                ],
            }
        )
        cls.fiscal_position2 = cls.env["account.fiscal.position"].create(
            {
                "name": "Test declaration 2",
                "valid_for_declaration_of_intent": False,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": cls.tax22.id,
                            "tax_dest_id": cls.tax10.id,
                        },
                    )
                ],
            }
        )

        cls.declaration1 = cls._create_declaration(cls.partner1, "out")
        cls.declaration2 = cls._create_declaration(cls.partner2, "out")
        cls.declaration3 = cls._create_declaration(cls.partner2, "out")
        cls.env["l10n_it_declaration_of_intent.yearly_limit"].create(
            {
                "year": cls.today_date.year,
                "limit_amount": 50000.0,
                "company_id": cls.env.company.id,
            }
        )
        cls.declaration4 = cls._create_declaration(cls.partner4, "in")
        cls.invoice1 = cls._create_invoice("1", cls.partner1)
        cls.invoice2 = cls._create_invoice("2", cls.partner1, tax=cls.tax1)
        cls.invoice3 = cls._create_invoice("3", cls.partner1, tax=cls.tax1)
        cls.invoice_without_valid_taxes = cls._create_invoice(
            "no valid taxes", cls.partner1, tax=cls.tax2
        )
        future_date = datetime.today() + timedelta(days=10)
        future_date = future_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        cls.invoice_future = cls._create_invoice(
            "future", cls.partner1, date=future_date, tax=cls.tax1
        )
        cls.out_refund = cls._create_refund(cls.partner1, tax=cls.tax1)
        cls.in_refund = cls._create_refund(
            cls.partner1,
            tax=cls.tax1,
            in_type=True,
        )
        cls.invoice4 = cls._create_invoice("4", cls.partner3, tax=cls.tax22)
        cls.invoice4.fiscal_position_id = cls.fiscal_position2.id
        cls.invoice5 = cls._create_invoice(
            "5", cls.partner4, tax=cls.tax1, in_type=True
        )

    def test_declaration_data(self):
        self.assertTrue(self.declaration1.number)

    def test_costraints(self):
        with self.assertRaises(ValidationError):
            self.declaration1.fiscal_position_id = (
                self.fiscal_position_with_wrong_taxes.id
            )

    def test_get_valid(self):
        declaration_model = self.env["l10n_it_declaration_of_intent.declaration"]
        self.assertFalse(declaration_model.get_valid())
        records = declaration_model.get_valid(
            type_d="out", partner_id=self.partner1.id, date=self.today_date
        )
        self.assertEqual(len(records), 1)
        records = declaration_model.get_valid(
            type_d="out", partner_id=self.partner2.id, date=self.today_date
        )
        self.assertEqual(len(records), 2)

    def test_declaration_state_change(self):
        self.assertEqual(self.declaration1.state, "valid")
        # Close declaration by moving end date before today
        previuos_date = datetime.today() - timedelta(days=10)
        self.declaration1.date_start = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT
        )
        self.declaration1.date_end = previuos_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        self.assertEqual(self.declaration1.state, "expired")

    def test_invoice_validation_with_no_effect_on_declaration(self):
        previous_used_amount = self.declaration1.used_amount
        self.invoice1.action_post()
        post_used_amount = self.declaration1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_future.action_post()
        post_used_amount = self.declaration1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_without_valid_taxes.action_post()
        post_used_amount = self.declaration1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_reopen_with_no_effect_on_declaration(self):
        previous_used_amount = self.declaration1.used_amount
        self.invoice1.action_post()
        self.invoice1.button_cancel()
        post_used_amount = self.declaration1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_under_declaration_limit(self):
        previous_used_amount = self.declaration1.used_amount
        self.invoice2.action_post()
        post_used_amount = self.declaration1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_over_declaration_limit(self):
        self.invoice2.action_post()
        with self.assertRaises(UserError):
            self.invoice3.action_post()

    def test_invoice_reopen_with_effect_on_declaration(self):
        previous_used_amount = self.declaration1.used_amount
        self.invoice2.action_post()
        self.invoice2.button_cancel()
        post_used_amount = self.declaration1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_refund(self):
        self.invoice2.action_post()
        previous_used_amount = self.declaration1.used_amount
        self.out_refund.action_post()
        post_used_amount = self.declaration1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_refund_with_amount_bigger_than_residual(self):
        self.invoice2.action_post()
        refund_form = Form(self.out_refund)
        with refund_form.invoice_line_ids.edit(0) as line_form:
            line_form.quantity = 10
        refund_form.save()

        # Check that base amount has been updated
        self.assertEqual(self.out_refund.amount_untaxed, 1000)

        # Refund goes over plafond: 100 + 1000 > 1000
        self.assertEqual(self.declaration1.available_amount, 100)
        self.assertEqual(self.out_refund.amount_untaxed, 1000)
        self.assertEqual(self.declaration1.limit_amount, 1000)
        with self.assertRaises(UserError):
            self.out_refund.action_post()

    def test_fiscal_position_no_declaration(self):
        self.invoice4._onchange_date_invoice()
        self.assertEqual(self.invoice4.fiscal_position_id.id, self.fiscal_position2.id)

    def test_invoice_vendor_with_no_effect_on_declaration(self):
        previous_used_amount = self.declaration4.used_amount
        self.assertAlmostEqual(previous_used_amount, 0.0, 2)
        self.invoice5.action_post()
        post_used_amount = self.declaration4.used_amount
        self.assertAlmostEqual(post_used_amount, 900.0, 2)

    def test_all_invoice_types(self):
        """
        Check that a declaration with all the invoice types
        computes the totals correctly.
        """
        partner = self.partner1

        out_invoice = self._create_invoice(
            "test_all_out_invoice", partner, tax=self.tax1, in_type=False
        )
        self.assertEqual(out_invoice.move_type, "out_invoice")
        out_invoice_balance = out_invoice.line_ids.filtered("tax_ids").balance
        self.assertEqual(out_invoice_balance, -900)

        in_invoice = self._create_invoice(
            "test_all_in_invoice", partner, tax=self.tax1, in_type=True
        )
        self.assertEqual(in_invoice.move_type, "in_invoice")
        in_invoice_balance = in_invoice.line_ids.filtered("tax_ids").balance
        self.assertEqual(in_invoice_balance, 900)

        out_refund = self._create_refund(partner, tax=self.tax1, in_type=False)
        self.assertEqual(out_refund.move_type, "out_refund")
        out_refund_balance = out_refund.line_ids.filtered("tax_ids").balance
        self.assertEqual(out_refund_balance, 100)

        in_refund = self._create_refund(partner, tax=self.tax1, in_type=True)
        self.assertEqual(in_refund.move_type, "in_refund")
        in_refund_balance = in_refund.line_ids.filtered("tax_ids").balance
        self.assertEqual(in_refund_balance, -100)

        invoices = out_invoice | in_invoice | out_refund | in_refund

        declaration = self._create_declaration(partner, "out")
        declaration.limit_amount = 2000
        invoices.declaration_of_intent_ids = declaration

        invoices.action_post()
        used_amount = (
            -out_invoice_balance
            + in_invoice_balance
            - out_refund_balance
            + in_refund_balance
        )
        self.assertEqual(declaration.available_amount, 2000 - used_amount)
