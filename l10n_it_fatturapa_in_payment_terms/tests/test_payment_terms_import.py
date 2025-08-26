# Copyright 2025 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import (
    FatturapaCommon
)
from datetime import date


class TestPaymentTermsImport(FatturapaCommon):

    def setUp(self):
        super(TestPaymentTermsImport, self).setUp()
        self.invoice_model = self.env['account.invoice']
        # Use existing payment term from account module
        self.payment_term = self.env.ref('account.account_payment_term')
        # Create withholding tax for tests that need it
        self.wt = self.create_wt()

    def test_payment_terms_from_xml(self):
        """Test that payment terms are correctly extracted from FatturaPA 
        and account.move.line entries are created with correct due dates.
        The test verifies that the validated invoice has 2 account.move.line 
        entries with due dates 2015-01-28 and 2015-02-28."""
        
        # Run the import wizard to create the invoice from XML
        res = self.run_wizard(
            'test_payment_terms', 
            'IT01234567890_FPR03.xml',
            module_name='l10n_it_fatturapa_in_payment_terms'
        )
        
        # Get the created invoices
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)

        # we need to convert because we need to validate the invoice and compare amounts
        invoices.write({"currency_id": self.env.user.company_id.currency_id.id})
        
        # Find the invoice that has payment data
        # (The XML may contain multiple invoices, we need the one with split payments)
        invoice_with_payments = None
        for invoice in invoices:
            if invoice.fatturapa_payments and len(invoice.fatturapa_payments.payment_methods) > 1:
                invoice_with_payments = invoice
                break
        
        self.assertTrue(invoice_with_payments, 
                       "No invoice found with multiple payment terms in FatturaPA data")
        
        # Set a payment term on the invoice and enable XML retrieval
        invoice_with_payments.payment_term_id = self.payment_term
        # Enable payment terms retrieval from XML for this payment term
        self.payment_term.fatturapa_retrieve_due_dates = True
        
        # Validate the invoice to create account moves
        invoice_with_payments.action_invoice_open()
        
        # Check that the invoice has been validated
        self.assertEqual(invoice_with_payments.state, 'open',
                        "Invoice should be in 'open' state after validation")
        
        # Check the account move lines
        self.assertTrue(invoice_with_payments.move_id,
                       "Invoice should have an account move after validation")
        
        # Get the payable move lines (those with account_id = partner's payable account)
        payable_lines = invoice_with_payments.move_id.line_ids.filtered(
            lambda l: l.account_id == invoice_with_payments.account_id
        )
        
        # Must have exactly 2 payable lines for the split payment
        self.assertEqual(len(payable_lines), 2,
                        "Invoice must have exactly 2 account.move.line entries for payables")
        
        # Sort by date maturity to ensure consistent order
        payable_lines = payable_lines.sorted('date_maturity')
        
        # Check first payment line - due date must be 2015-01-28
        self.assertEqual(
            payable_lines[0].date_maturity, 
            date(2015, 1, 28),
            "First payment line must have due date 2015-01-28"
        )
        
        # Check second payment line - due date must be 2015-02-28
        self.assertEqual(
            payable_lines[1].date_maturity,
            date(2015, 2, 28),
            "Second payment line must have due date 2015-02-28"
        )
        
        # Verify that payment amounts are reasonable (greater than 0)
        for line in payable_lines:
            amount = abs(line.credit or line.debit)
            self.assertGreater(amount, 0,
                              "Payment line amount must be greater than 0")
        
        # Check that total of payable lines matches invoice total
        total_payable = sum(abs(l.credit or l.debit) for l in payable_lines)
        self.assertAlmostEqual(
            total_payable,
            invoice_with_payments.amount_total,
            places=2,
            msg="Total of payment lines must match invoice total"
        )

    def test_payment_terms_disabled(self):
        """Test that standard payment terms are used when XML retrieval is disabled."""
        
        # Run the import wizard
        res = self.run_wizard(
            'test_payment_disabled', 
            'IT01234567890_FPR04.xml',
            module_name='l10n_it_fatturapa_in_payment_terms'
        )
        
        # Get the created invoices
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        invoices.write({"currency_id": self.env.user.company_id.currency_id.id})
        
        # Find an invoice with payment data
        invoice_with_payments = None
        for invoice in invoices:
            if invoice.fatturapa_payments:
                invoice_with_payments = invoice
                break
        
        self.assertTrue(invoice_with_payments,
                       "No invoice found with payment data")
        
        # Set payment term with XML retrieval disabled (default is False)
        invoice_with_payments.payment_term_id = self.payment_term
        self.payment_term.fatturapa_retrieve_due_dates = False
        
        # Validate the invoice
        invoice_with_payments.action_invoice_open()
        
        # Check that standard payment term was used (single payment)
        payable_lines = invoice_with_payments.move_id.line_ids.filtered(
            lambda l: l.account_id == invoice_with_payments.account_id
        )
        
        # Should have only 1 payable line when using standard payment term
        # (not using the XML payment data)
        self.assertEqual(len(payable_lines), 1,
                        "When XML retrieval is disabled, should use standard payment term with single payment")

    def test_payment_terms_partial_payment(self):
        """Test that when payment details total is less than e_invoice_amount_total,
        an additional line without due date is created for the remaining amount.

        This test uses an invoice with:
        - Total amount: 427.00 EUR
        - Payment amount in XML: 357.00 EUR
        - Expected remaining amount: 70.00 EUR (withholding tax)
        """

        # Run the import wizard with XML that has partial payment
        res = self.run_wizard(
            'test_partial_payment',
            'IT10538570960_FPR05.xml',
            module_name='l10n_it_fatturapa_in_payment_terms'
        )

        # Get the created invoices
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        invoices.write({"currency_id": self.env.user.company_id.currency_id.id})

        # Get the invoice (should be only one in this XML)
        self.assertEqual(len(invoices), 1,
                        "Should have exactly 1 invoice from the test XML")
        invoice_with_payments = invoices[0]

        # Verify the invoice has payment data
        self.assertTrue(invoice_with_payments.fatturapa_payments,
                       "Invoice should have payment data")

        # Verify e_invoice_amount_total and payment amount
        self.assertAlmostEqual(invoice_with_payments.e_invoice_amount_total, 427.00, places=2)
        payment_amount = sum(p.payment_amount for p in invoice_with_payments.fatturapa_payments.payment_methods)
        self.assertAlmostEqual(payment_amount, 357.00, places=2,
                              msg="Payment amount from XML should be 357.00")

        # Set payment term with XML retrieval enabled
        invoice_with_payments.payment_term_id = self.payment_term
        self.payment_term.fatturapa_retrieve_due_dates = True

        # Validate the invoice
        invoice_with_payments.action_invoice_open()

        # Check that the invoice has been validated
        self.assertEqual(invoice_with_payments.state, 'open',
                        "Invoice should be in 'open' state after validation")

        # Get the payable move lines
        payable_lines = invoice_with_payments.move_id.line_ids.filtered(
            lambda l: l.account_id == invoice_with_payments.account_id
        )

        # Should have 2 payable lines: 1 with XML due date + 1 with invoice date (remainder)
        self.assertEqual(len(payable_lines), 2,
                               "Invoice should have 2 payable lines")

        # Sort payable lines by date_maturity for consistent order
        payable_lines = payable_lines.sorted('date_maturity')

        # First line should be the remainder line with invoice date (2025-10-03) and amount 70.00
        remainder_line = payable_lines[0]
        self.assertEqual(
            remainder_line.date_maturity,
            date(2025, 10, 3),
            "Remainder line should have invoice date as maturity date (2025-10-03)"
        )
        self.assertAlmostEqual(
            abs(remainder_line.credit or remainder_line.debit),
            70.00,
            places=2,
            msg="Remainder line should have amount 70.00"
        )

        # Second line should be the XML payment line with due date 2025-10-10 and amount 357.00
        xml_payment_line = payable_lines[1]
        self.assertEqual(
            xml_payment_line.date_maturity,
            date(2025, 10, 10),
            "XML payment line should have due date from XML (2025-10-10)"
        )
        self.assertAlmostEqual(
            abs(xml_payment_line.credit or xml_payment_line.debit),
            357.00,
            places=2,
            msg="XML payment line should have amount 357.00"
        )

        # Verify total of payable lines matches invoice total
        total_payable = sum(abs(l.credit or l.debit) for l in payable_lines)
        self.assertAlmostEqual(
            total_payable,
            invoice_with_payments.amount_total,
            places=2,
            msg="Total of payment lines must match invoice total"
        )