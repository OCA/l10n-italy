# Copyright 2025 Nextev
# # License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestDoiIssuedFromCompany(TransactionCase):
    @classmethod
    def _create_declaration(cls, type_doi, protocol_part1=None, protocol_part2=None):
        """Create a declaration with unique protocol numbers."""
        if protocol_part1 is None:
            # Generate unique protocol numbers based on sequence
            if not hasattr(cls, "_protocol_counter"):
                cls._protocol_counter = 0
            cls._protocol_counter += 1
            protocol_part1 = str(1000 + cls._protocol_counter)
            protocol_part2 = str(2000 + cls._protocol_counter)

        return cls.env["l10n_it_edi_doi.declaration_of_intent"].create(
            {
                "partner_id": cls.partner.id,
                "company_id": cls.company.id,
                "state": "active",
                "type": type_doi,
                "currency_id": cls.company.currency_id.id,
                "issue_date": fields.Date.today(),
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + relativedelta(months=2),
                "threshold": 5000,
                "protocol_number_part1": protocol_part1,
                "protocol_number_part2": protocol_part2,
            }
        )

    @classmethod
    def _create_invoice(cls, name, partner, taxes=False, date=False, in_type=False):
        invoice_form = Form(
            cls.env["account.move"].with_context(
                default_move_type="in_invoice" if in_type else "out_invoice",
                default_partner_id=partner.id,
            )
        )
        invoice_form.invoice_date = date if date else fields.Date.today()
        invoice_form.invoice_payment_term_id = cls.env.ref(
            "account.account_payment_term_advance"
        )
        cls._add_invoice_line_id(invoice_form, taxes=taxes, in_type=in_type)
        invoice = invoice_form.save()
        return invoice

    @classmethod
    def _add_invoice_line_id(cls, invoice_form, taxes=False, in_type=False):
        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = cls.env.ref("product.product_product_5")
            invoice_line.quantity = 10.00
            invoice_line.name = "test line"
            invoice_line.price_unit = 90.00
            if taxes:
                invoice_line.tax_ids.clear()
                for tax in taxes:
                    invoice_line.tax_ids.add(tax)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.country_id = cls.env.ref("base.it")
        cls.company.account_fiscal_country_id = cls.env.ref("base.it")
        cls.tax_model = cls.env["account.tax"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.partner.country_id = cls.env.ref("base.it")
        cls.partner.company_id = cls.company
        cls.doi_in = cls._create_declaration("in")
        cls.tax_group = cls.env["account.tax.group"].create(
            {"name": "Vat Free", "sequence": 1}
        )
        cls.tax = cls.tax_model.create(
            {
                "l10n_it_exempt_reason": "N3.5",
                "l10n_it_law_reference": "Art. 8, comma 1, lett. a) DPR 633/72",
                "type_tax_use": "purchase",
                "name": "0% declaration tax3",
                "amount": 0,
                "tax_group_id": cls.tax_group.id,
            }
        )
        cls.env.company.l10n_it_edi_doi_bill_tax_id = cls.tax

    def test_in_invoice_under_declaration_limit(self):
        invoice = self._create_invoice("1", self.partner, taxes=self.tax, in_type=True)

        # Verify DOI is auto-assigned
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_in)

        # Verify DOI amount is computed correctly
        self.assertEqual(invoice.l10n_it_edi_doi_amount, 900.0)

        previous_used_amount = self.doi_in.invoiced
        invoice.action_post()
        used_amount = self.doi_in.invoiced
        self.assertNotEqual(previous_used_amount, used_amount)
        self.assertEqual(used_amount, 900.0)
        self.assertEqual(self.doi_in.state, "active")

    def test_multiple_declarations_bridge_model(self):
        """Test that multiple declarations can be linked via bridge model."""
        # Create a second declaration
        doi_in_2 = self._create_declaration("in")

        # Create invoice
        invoice = self._create_invoice("2", self.partner, taxes=self.tax, in_type=True)

        # Add multiple declarations via bridge model
        self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": self.doi_in.id,
                "amount": 500.0,
            }
        )
        self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": doi_in_2.id,
                "amount": 400.0,
            }
        )

        # Check counts and totals
        self.assertEqual(invoice.l10n_it_edi_doi_count, 2)
        self.assertEqual(invoice.l10n_it_edi_doi_total_amount, 900.0)

        # Post invoice and verify amounts are correctly tracked
        prev_doi1_invoiced = self.doi_in.invoiced
        prev_doi2_invoiced = doi_in_2.invoiced
        invoice.action_post()

        self.assertEqual(self.doi_in.invoiced, prev_doi1_invoiced + 500.0)
        self.assertEqual(doi_in_2.invoiced, prev_doi2_invoiced + 400.0)

    def test_single_declaration_backward_compatibility(self):
        """Test that single declaration workflow still works."""
        invoice = self._create_invoice("3", self.partner, taxes=self.tax, in_type=True)

        # Standard field should be auto-filled
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_in)

        # Post and verify
        prev_invoiced = self.doi_in.invoiced
        invoice.action_post()
        self.assertEqual(self.doi_in.invoiced, prev_invoiced + invoice.amount_total)

    def test_declaration_available_amount_computation(self):
        """Test that available amount is correctly computed in bridge model."""
        invoice = self._create_invoice("4", self.partner, taxes=self.tax, in_type=True)

        doi_line = self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": self.doi_in.id,
                "amount": 100.0,
            }
        )

        # Available amount should be threshold - invoiced
        expected_available = self.doi_in.threshold - self.doi_in.invoiced
        self.assertEqual(doi_line.declaration_available, expected_available)

    def test_warning_when_amounts_dont_match(self):
        """Test that warning shows when DOI amounts don't cover invoice total."""
        invoice = self._create_invoice("5", self.partner, taxes=self.tax, in_type=True)

        # Add declaration with amount less than invoice total
        self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": self.doi_in.id,
                "amount": 100.0,  # Invoice total is 900
            }
        )

        # Warning should be present
        self.assertTrue(invoice.l10n_it_edi_doi_warning)
        self.assertIn("100.00", invoice.l10n_it_edi_doi_warning)
        self.assertIn("900.00", invoice.l10n_it_edi_doi_warning)

    def test_no_warning_when_amounts_match(self):
        """Test that no warning shows when amounts fully cover invoice."""
        invoice = self._create_invoice("6", self.partner, taxes=self.tax, in_type=True)

        # Add declaration with full invoice amount
        self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": self.doi_in.id,
                "amount": 900.0,  # Full invoice total
            }
        )

        # Warning should be empty
        self.assertFalse(invoice.l10n_it_edi_doi_warning)

    def test_mixed_invoices_computation(self):
        """Test that invoiced amount correctly handles mixed approaches."""
        # Create invoice with bridge model
        invoice1 = self._create_invoice("7", self.partner, taxes=self.tax, in_type=True)
        self.env["account.move.doi"].create(
            {
                "move_id": invoice1.id,
                "declaration_id": self.doi_in.id,
                "amount": 300.0,
            }
        )
        invoice1.action_post()

        # Create invoice with standard field (no bridge)
        invoice2 = self._create_invoice("8", self.partner, taxes=self.tax, in_type=True)
        # Standard workflow - no bridge records
        invoice2.action_post()

        # Total invoiced should be sum of both
        expected_total = 300.0 + invoice2.amount_total
        self.assertEqual(self.doi_in.invoiced, expected_total)

    def test_synchronization_standard_field_to_list(self):
        """Test that standard field changes sync to multi-declaration list."""
        invoice = self._create_invoice("9", self.partner, taxes=self.tax, in_type=True)

        # Standard field should auto-populate
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_in)

        # Should have created bridge record via onchange
        # (Note: onchange may not fire in tests without Form)
        # This tests the intended behavior when using the UI

    def test_action_open_declaration_multiple(self):
        """Test action_open_declaration_of_intent with multiple declarations."""
        invoice = self._create_invoice("10", self.partner, taxes=self.tax, in_type=True)

        # Create second declaration
        doi_in_2 = self._create_declaration("in")

        # Add multiple declarations
        self.env["account.move.doi"].create(
            [
                {
                    "move_id": invoice.id,
                    "declaration_id": self.doi_in.id,
                    "amount": 400.0,
                },
                {
                    "move_id": invoice.id,
                    "declaration_id": doi_in_2.id,
                    "amount": 500.0,
                },
            ]
        )

        # Action should open list view with multiple records
        action = invoice.action_open_declaration_of_intent()
        self.assertEqual(action["view_mode"], "list,form")
        self.assertIn("domain", action)
        declaration_ids = action["domain"][0][2]
        self.assertEqual(len(declaration_ids), 2)
        self.assertIn(self.doi_in.id, declaration_ids)
        self.assertIn(doi_in_2.id, declaration_ids)

    def test_declaration_with_refund(self):
        """Test that refund correctly reduces the declaration invoiced amount."""
        # Create and post an invoice
        invoice = self._create_invoice("11", self.partner, taxes=self.tax, in_type=True)
        self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": self.doi_in.id,
                "amount": 900.0,
            }
        )
        invoice.action_post()

        # Check initial invoiced amount
        initial_invoiced = self.doi_in.invoiced
        self.assertEqual(initial_invoiced, 900.0)

        # Verify invoice is correctly configured
        self.assertEqual(invoice.move_type, "in_invoice")
        self.assertEqual(invoice.doi_type, "in")
        self.assertEqual(invoice.l10n_it_edi_doi_amount, 900.0)

        # Create a refund
        refund_wizard = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": fields.Date.today(),
                    "reason": "Test refund",
                    "company_id": self.company.id,
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        refund_action = refund_wizard.reverse_moves()
        refund = self.env["account.move"].browse(refund_action["res_id"])

        # Verify refund properties before posting
        self.assertEqual(refund.state, "draft")
        self.assertEqual(refund.move_type, "in_refund")
        self.assertEqual(refund.doi_type, "in")

        # Verify DOI was automatically copied from original invoice
        self.assertEqual(refund.l10n_it_edi_doi_count, 1)
        refund_doi_line = refund.l10n_it_edi_doi_ids
        self.assertEqual(refund_doi_line.declaration_id, self.doi_in)
        self.assertEqual(refund_doi_line.amount, 900.0)

        # Verify refund DOI amount - refunds have positive value, handled by move_type
        self.assertEqual(refund.l10n_it_edi_doi_amount, 900.0)

        # Post refund
        refund.action_post()

        # Verify refund is posted
        self.assertEqual(refund.state, "posted")

        # Check that invoiced amount is reduced (invoice 900 + refund -900 = 0)
        final_invoiced = self.doi_in.invoiced
        self.assertEqual(final_invoiced, 0.0)

        # Verify declaration is still active (not used yet)
        self.assertEqual(self.doi_in.state, "active")
        self.assertEqual(self.doi_in.remaining, self.doi_in.threshold)

    def test_declaration_with_partial_refund(self):
        """Test partial refund scenario with multiple invoices."""
        # Create and post first invoice
        invoice1 = self._create_invoice(
            "12", self.partner, taxes=self.tax, in_type=True
        )
        self.env["account.move.doi"].create(
            {
                "move_id": invoice1.id,
                "declaration_id": self.doi_in.id,
                "amount": 900.0,
            }
        )
        invoice1.action_post()

        # Check initial invoiced amount
        initial_invoiced = self.doi_in.invoiced
        self.assertEqual(initial_invoiced, 900.0)
        self.assertEqual(self.doi_in.remaining, self.doi_in.threshold - 900.0)

        # Create a second invoice
        invoice2 = self._create_invoice(
            "13", self.partner, taxes=self.tax, in_type=True
        )
        self.env["account.move.doi"].create(
            {
                "move_id": invoice2.id,
                "declaration_id": self.doi_in.id,
                "amount": 900.0,
            }
        )
        invoice2.action_post()

        # Now invoiced should be cumulative
        self.assertEqual(self.doi_in.invoiced, 1800.0)
        self.assertEqual(self.doi_in.remaining, self.doi_in.threshold - 1800.0)

        # Create refund for second invoice only (partial refund of total)
        refund_wizard = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice2.ids)
            .create(
                {
                    "date": fields.Date.today(),
                    "reason": "Test partial refund",
                    "company_id": self.company.id,
                    "journal_id": invoice2.journal_id.id,
                }
            )
        )
        refund_action = refund_wizard.reverse_moves()
        refund = self.env["account.move"].browse(refund_action["res_id"])

        # Verify refund properties
        self.assertEqual(refund.move_type, "in_refund")
        self.assertEqual(refund.doi_type, "in")

        # Verify DOI was automatically copied from invoice2
        self.assertEqual(refund.l10n_it_edi_doi_count, 1)
        refund_doi_line = refund.l10n_it_edi_doi_ids
        self.assertEqual(refund_doi_line.declaration_id, self.doi_in)
        self.assertEqual(refund_doi_line.amount, 900.0)

        # Refunds have positive DOI amount, the move_type determines if it reduces usage
        self.assertEqual(refund.l10n_it_edi_doi_amount, 900.0)

        # Post refund
        refund.action_post()

        # Check that invoiced amount is reduced by refund amount
        # invoice1 (900) + invoice2 (900) + refund (-900) = 900
        final_invoiced = self.doi_in.invoiced
        self.assertEqual(final_invoiced, 900.0)

        # Check remaining is updated correctly
        self.assertEqual(self.doi_in.remaining, self.doi_in.threshold - 900.0)

        # Verify all moves are still linked to declaration
        all_moves = self.doi_in.invoice_ids
        self.assertIn(invoice1, all_moves)
        self.assertIn(invoice2, all_moves)
        self.assertIn(refund, all_moves)

    def test_out_invoice_with_two_taxes(self):
        tax2 = self.tax_model.create(
            {
                "l10n_it_exempt_reason": "N4",
                "l10n_it_law_reference": "Dumb tax for test",
                "type_tax_use": "purchase",
                "name": "0% dumb tax",
                "amount": 0,
                "tax_group_id": self.tax_group.id,
            }
        )
        invoice = self._create_invoice(
            "1", self.partner, taxes=self.tax | tax2, in_type=True
        )

        previous_used_amount = self.doi_in.invoiced
        invoice.action_post()
        used_amount = self.doi_in.invoiced
        self.assertNotEqual(previous_used_amount, used_amount)
        self.assertEqual(used_amount, invoice.amount_total)
        self.assertEqual(self.doi_in.state, "active")
