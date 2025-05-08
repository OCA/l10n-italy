# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestDeclarationOfIntent(AccountTestInvoicingCommon):
    @classmethod
    def _create_declaration(cls, partner, type_d):
        return cls.env["l10n_it_declaration_of_intent.declaration"].create(
            {
                "partner_id": partner.id,
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
        invoice_form.invoice_payment_term_id = cls.env.ref(
            "account.account_payment_term_advance"
        )
        cls._add_invoice_line_id(invoice_form, tax=tax, in_type=in_type)
        invoice = invoice_form.save()
        return invoice

    @classmethod
    def _add_invoice_line_id(cls, invoice_form, tax=False, in_type=False):
        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = cls.env.ref("product.product_product_5")
            invoice_line.quantity = 10.00
            invoice_line.account_id = cls.a_cost if in_type else cls.a_sale
            invoice_line.name = "test line"
            invoice_line.price_unit = 90.00
            if tax:
                invoice_line.tax_ids.clear()
                invoice_line.tax_ids.add(tax)

    @classmethod
    def _create_refund(cls, partner, tax=False, date=False, in_type=False):
        refund_form = Form(
            cls.env["account.move"].with_context(
                default_move_type="in_refund" if in_type else "out_refund"
            )
        )
        refund_form.partner_id = partner
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
                    "account_type",
                    "=",
                    "income",
                )
            ],
            limit=1,
        )
        cls.a_cost = cls.env["account.account"].search(
            [
                (
                    "account_type",
                    "=",
                    "expense_direct_cost",
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
        cls.other_company = cls.env["res.company"].create(
            {
                "name": "other",
            }
        )
        cls.other_user = cls.env["res.users"].create(
            {
                "name": "User of other company",
                "login": "other",
                "company_ids": [
                    (4, cls.other_company.id),
                ],
                "company_id": cls.other_company.id,
            }
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

    def test_multiple_invoices(self):
        """Check that validating multiple invoices
        when there is no valid declaration raises an error."""
        self.declaration1.unlink()
        invoices = self.invoice1 | self.invoice2
        with self.assertRaises(UserError) as ue:
            invoices.action_post()
        self.assertIn("Declaration of intent not found", ue.exception.args[0])

    def test_invoice_vendor_with_no_effect_on_declaration(self):
        previous_used_amount = self.declaration4.used_amount
        self.assertAlmostEqual(previous_used_amount, 0.0, 2)
        self.invoice5.action_post()
        post_used_amount = self.declaration4.used_amount
        self.assertAlmostEqual(post_used_amount, 900.0, 2)

    def test_all_invoice_types(self):
        """
        Check that declarations with both invoices and refunds compute
        the totals correctly.
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

        declaration_out = self._create_declaration(partner, "out")
        declaration_out.limit_amount = 2000
        invoices_in = in_invoice | in_refund
        invoices_in.declaration_of_intent_ids = declaration_out

        declaration_in = self._create_declaration(partner, "in")
        declaration_in.limit_amount = 2000
        invoices_out = out_invoice | out_refund
        invoices_out.declaration_of_intent_ids = declaration_in

        invoices_in.action_post()
        invoices_out.action_post()

        # balance is positive for in invoices
        # add "in" invoice and refund and compare with "out" DI available_amount
        used_amount_in = in_invoice_balance + in_refund_balance
        self.assertEqual(used_amount_in, 800)
        self.assertEqual(declaration_out.available_amount, 2000 - used_amount_in)

        # balance is positive for out invoices
        # add "out" invoice and refund and compare with "in" DI available_amount
        used_amount_out = -out_invoice_balance - out_refund_balance
        self.assertEqual(used_amount_out, 800)
        self.assertEqual(declaration_in.available_amount, 2000 - used_amount_out)

    def test_invoice_repost(self):
        invoice = self._create_invoice(
            "test_invoice_repost", self.partner1, tax=self.tax1
        )
        invoice_form = Form(invoice)
        for tax in (self.tax2, self.tax22):
            self._add_invoice_line_id(invoice_form, tax=tax)
        invoice = invoice_form.save()
        invoice.action_post()
        invoice.button_draft()
        invoice.action_post()
        self.assertEqual(
            len(
                self.declaration1.line_ids.filtered(
                    lambda line: line.invoice_id == invoice
                )
            ),
            1,
        )

    def test_invoice_delete(self):
        invoice = self._create_invoice(
            "test_invoice_repost", self.partner1, tax=self.tax1
        )
        invoice_form = Form(invoice)
        for tax in (self.tax2, self.tax22):
            self._add_invoice_line_id(invoice_form, tax=tax)
        invoice = invoice_form.save()
        invoice.action_post()
        invoice.button_draft()
        invoice.unlink()
        self.assertEqual(
            len(
                self.declaration1.line_ids.filtered(
                    lambda line: line.invoice_id == invoice
                )
            ),
            0,
        )

    def test_multi_company(self):
        """Check that a user can only see and create declarations in his company."""
        self.env = self.env(user=self.other_user)
        declaration_model = self.env["l10n_it_declaration_of_intent.declaration"]

        # See only declarations in current company
        self.assertFalse(declaration_model.search_count([]))

        # Create tax_id in other company
        other_tax10 = self.env["account.tax"].create(
            {
                "name": "10%",
                "amount": 10,
                "country_id": self.env.ref("base.it").id,
            }
        )
        other_tax1 = self.env["account.tax"].create(
            {
                "name": "FC INC",
                "amount": 0,
                "price_include": True,
                "country_id": self.env.ref("base.it").id,
            }
        )

        # Create fiscal_position in other company
        fiscal_position2 = self.env["account.fiscal.position"].create(
            {
                "name": "Test Fiscal Position2",
                "valid_for_declaration_of_intent": False,
                "tax_ids": [
                    (
                        0,
                        0,
                        {
                            "tax_src_id": other_tax10.id,
                            "tax_dest_id": other_tax1.id,
                        },
                    )
                ],
            }
        )

        # Create declaration in other company
        declaration = self.env["l10n_it_declaration_of_intent.declaration"].create(
            {
                "partner_id": self.partner1.id,
                "partner_document_number": "PartnerTest%s" % self.partner1.id,
                "partner_document_date": self.today_date,
                "date": self.today_date,
                "date_start": self.today_date,
                "date_end": self.today_date,
                "taxes_ids": [(6, 0, [other_tax1.id])],
                "limit_amount": 1000.00,
                "fiscal_position_id": fiscal_position2.id,
                "type": "out",
                "telematic_protocol": "08060120341234567-000001",
            }
        )
        self.assertEqual(declaration_model.search([]), declaration)
        self.assertEqual(self.env.company, declaration.company_id)

    def test_action_register_payment(self):
        """
        Check register payment from action in invoice.
        """
        partner = self.partner1
        partner.property_account_position_id = self.fiscal_position.id

        out_invoice = self._create_invoice(
            "test_out_invoice_registr_payment", partner, tax=self.tax1, in_type=False
        )
        self.assertEqual(out_invoice.move_type, "out_invoice")
        out_invoice.action_post()

        result = out_invoice.action_register_payment()
        wizard = Form(
            self.env[(result.get("res_model"))].with_context(**result["context"])
        ).save()
        self.assertEqual(wizard._name, "account.payment.register")
        action = wizard.action_create_payments()
        if action.get("res_id", False):
            payments = [action["res_id"]]
            self.assertTrue(len(payments) == 1)
        else:
            payments = action["domain"][0][2]
            self.assertTrue(len(payments) > 1)

    def test_multiple_valid(self):
        """
        Check multi declarations validation for same partner.
        """
        declaration_model = self.env["l10n_it_declaration_of_intent.declaration"].sudo()
        post_used_amount2 = self.declaration2.used_amount
        post_used_amount3 = self.declaration3.used_amount
        self.assertAlmostEqual(post_used_amount2, 0.0, 2)
        self.assertAlmostEqual(post_used_amount3, 0.0, 2)
        valid_declarations = declaration_model.get_valid(
            type_d="out", partner_id=self.partner2.id, date=self.today_date
        )
        self.assertEqual(valid_declarations, self.declaration2 | self.declaration3)
        invoice6 = self._create_invoice(
            "test_multiple_valid", self.partner2, tax=self.tax1
        )
        invoice6.action_post()
        new_post_used_amount2 = self.declaration2.used_amount
        new_post_used_amount3 = self.declaration3.used_amount
        self.assertAlmostEqual(new_post_used_amount2, 900.0, 2)
        self.assertAlmostEqual(new_post_used_amount3, 0.0, 2)
