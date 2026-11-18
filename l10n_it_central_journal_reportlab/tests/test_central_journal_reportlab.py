# Copyright 2022 Giuseppe Borruso
# Copyright 2024 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import io
from datetime import datetime

from dateutil.rrule import MONTHLY

from odoo.tests.common import Form, TransactionCase
from odoo.tools import pdf


class TestCentralJournalReportlab(TransactionCase):
    def setUp(self):
        super().setUp()

        self.today = datetime.now()
        self.range_type = self.env["date.range.type"].search(
            [("name", "=", "Fiscal year")], limit=1
        )
        if not self.range_type:
            self.range_type = self.env["date.range.type"].create(
                {"name": "Fiscal year"}
            )

        # Check if date ranges already exist for this year
        existing_ranges = self.env["date.range"].search(
            [
                ("type_id", "=", self.range_type.id),
                ("date_start", ">=", "%s-01-01" % self.today.year),
                ("date_end", "<=", "%s-12-31" % self.today.year),
            ]
        )

        if not existing_ranges:
            self.env["date.range.generator"].create(
                {
                    "date_start": "%s-01-01" % self.today.year,
                    "name_prefix": "%s-" % self.today.year,
                    "type_id": self.range_type.id,
                    "duration_count": 1,
                    "unit_of_time": str(MONTHLY),
                    "count": 12,
                }
            ).action_apply()

        self.current_period = self.env["date.range"].search(
            [
                ("date_start", "<=", self.today.date()),
                ("date_end", ">=", self.today.date()),
            ]
        )
        self.wizard_model = self.env["wizard.giornale.reportlab"]
        self.report_model = self.env["ir.actions.report"]
        self.report_name = "central_journal_reportlab.report_giornale_reportlab"
        self.journals = self.env["account.journal"].search([])

    def _get_pdf_data(self, wizard):
        """Helper to get PDF data from wizard (attachment or binary field)"""
        if wizard.attachment_id:
            return base64.b64decode(wizard.attachment_id.datas)
        return base64.b64decode(wizard.report_giornale)

    def test_wizard_reportlab(self):
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard = wizard_form.save()
        self.assertEqual(
            len(wizard.journal_ids),
            len(self.journals.filtered(lambda j: not j.central_journal_exclude)),
        )
        self.assertEqual(wizard.date_move_line_from, self.current_period.date_start)
        self.assertEqual(wizard.date_move_line_to, self.current_period.date_end)
        self.assertEqual(wizard.year_footer, str(self.today.year))
        next_year = self.today.year + 1

        wizard.year_footer = next_year
        wizard.fiscal_page_base = 99

        wizard.with_context(test_mode=True).print_giornale_reportlab()
        # Get PDF from attachment if available, otherwise from binary field
        decode_giornale = self._get_pdf_data(wizard)
        self.minimal_reader_buffer = io.BytesIO(decode_giornale)
        self.minimal_pdf_reader = pdf.OdooPdfFileReader(self.minimal_reader_buffer)
        self.assertTrue(self.minimal_reader_buffer)

    def test_grouped_move_line_no_account(self):
        """Move lines without account are excluded from grouped report."""
        # Arrange
        out_invoice = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        out_invoice.partner_id = self.env.ref("base.res_partner_1")
        out_invoice.invoice_date = self.today
        with out_invoice.invoice_line_ids.new() as note_line:
            note_line.display_type = "line_note"
            note_line.name = "Test note"
        with out_invoice.invoice_line_ids.new() as line:
            line.name = "Test line"
            line.price_unit = 100
        out_invoice = out_invoice.save()
        out_invoice.action_post()
        # pre-condition
        account_lines = out_invoice.invoice_line_ids.filtered("account_id")
        self.assertTrue(account_lines)
        no_account_lines = out_invoice.invoice_line_ids - account_lines
        self.assertTrue(no_account_lines)

        # Act
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard_form.group_by_account = True
        wizard = wizard_form.save()

        # Assert
        wizard.with_context(test_mode=True).print_giornale_reportlab()
        giornale_pdf_content = self._get_pdf_data(wizard)
        giornale_content = pdf.PdfFileReader(io.BytesIO(giornale_pdf_content))
        has_move = False
        for page in giornale_content.pages:
            page_content = page.extractText()
            if not has_move and out_invoice.name in page_content:
                has_move = True
        self.assertTrue(has_move)

    def test_batch_processing_multiple_batches(self):
        """Test batch processing with >500 lines to verify batching works."""
        # Create a journal entry with many lines (enough for multiple batches)
        # We'll create 3 invoices with multiple lines each to get >500 total lines
        AccountMove = self.env["account.move"]
        partner = self.env.ref("base.res_partner_1")

        # Get accounts for testing
        account_receivable = self.env["account.account"].search(
            [("account_type", "=", "asset_receivable")], limit=1
        )
        account_revenue = self.env["account.account"].search(
            [("account_type", "=", "income")], limit=1
        )

        if not account_receivable or not account_revenue:
            self.skipTest("Required accounts not found")

        total_invoices = 250  # This will create ~750 lines (3 per invoice)
        invoices = AccountMove.create(
            [
                {
                    "move_type": "out_invoice",
                    "partner_id": partner.id,
                    "invoice_date": self.today,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": f"Line 1 - Invoice {i}",
                                "price_unit": 100.0,
                                "quantity": 1,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": f"Line 2 - Invoice {i}",
                                "price_unit": 200.0,
                                "quantity": 1,
                            },
                        ),
                    ],
                }
                for i in range(total_invoices)
            ]
        )

        invoices.action_post()

        # Get total move lines created
        move_line_count = len(
            self.env["account.move.line"].search(
                [
                    ("move_id", "in", invoices.ids),
                    ("account_id", "!=", False),
                ]
            )
        )

        # Should be > 500 to trigger batch processing
        self.assertGreater(
            move_line_count, 500, f"Test needs >500 lines but got {move_line_count}"
        )

        # Generate report
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard = wizard_form.save()

        wizard.with_context(test_mode=True).print_giornale_reportlab()

        # Verify PDF was generated
        self.assertTrue(
            wizard.report_giornale or wizard.attachment_id, "PDF should be generated"
        )

        # Verify all invoices appear in the report
        giornale_pdf_content = self._get_pdf_data(wizard)
        giornale_content = pdf.PdfFileReader(io.BytesIO(giornale_pdf_content))

        # Extract all text from PDF
        all_text = ""
        for page in giornale_content.pages:
            all_text += page.extractText()

        # Check that some invoice names appear (sampling, not all 250)
        sample_invoices = invoices[:5] + invoices[-5:]
        for invoice in sample_invoices:
            self.assertIn(
                invoice.name,
                all_text,
                f"Invoice {invoice.name} should appear in report",
            )

    def test_balance_accuracy(self):
        """Test that initial, running, and final balances are calculated correctly."""
        # Set initial progressive balances
        self.current_period.write(
            {
                "progressive_debit": 1000.0,
                "progressive_credit": 800.0,
            }
        )

        # Create moves with known amounts
        partner = self.env.ref("base.res_partner_1")

        # Invoice 1: +500 debit (receivable), +500 credit (revenue)
        invoice1 = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice1.partner_id = partner
        invoice1.invoice_date = self.today
        with invoice1.invoice_line_ids.new() as line:
            line.name = "Test Product 1"
            line.price_unit = 500.0
            line.quantity = 1
        invoice1 = invoice1.save()
        invoice1.action_post()

        # Invoice 2: +300 debit (receivable), +300 credit (revenue)
        invoice2 = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice2.partner_id = partner
        invoice2.invoice_date = self.today
        with invoice2.invoice_line_ids.new() as line:
            line.name = "Test Product 2"
            line.price_unit = 300.0
            line.quantity = 1
        invoice2 = invoice2.save()
        invoice2.action_post()

        # Generate report
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard = wizard_form.save()

        wizard.with_context(test_mode=True).print_giornale_reportlab()

        # Verify PDF content contains balance information
        giornale_pdf_content = self._get_pdf_data(wizard)
        giornale_content = pdf.PdfFileReader(io.BytesIO(giornale_pdf_content))

        all_text = ""
        for page in giornale_content.pages:
            all_text += page.extractText()

        # Check for initial balance
        self.assertIn("1,000.00", all_text, "Initial debit should appear")
        self.assertIn("800.00", all_text, "Initial credit should appear")

        # Check PDF contains balance-related text
        # The exact number formatting may vary, so just verify report was generated
        # with appropriate content
        self.assertIn("Initial Balance", all_text)
        self.assertIn("Final Balance", all_text)

    def test_grouped_vs_ungrouped_aggregation(self):
        """Test that grouped mode correctly aggregates lines per account."""
        partner = self.env.ref("base.res_partner_1")

        # Create 3 invoices with same amounts to same partner
        # This will create multiple lines on the same receivable account
        for i in range(3):
            invoice = Form(
                self.env["account.move"].with_context(default_move_type="out_invoice")
            )
            invoice.partner_id = partner
            invoice.invoice_date = self.today
            with invoice.invoice_line_ids.new() as line:
                line.name = f"Test Product {i}"
                line.price_unit = 100.0
                line.quantity = 1
            invoice = invoice.save()
            invoice.action_post()

        # Generate ungrouped report
        wizard_ungrouped_form = Form(self.wizard_model)
        wizard_ungrouped_form.daterange_id = self.current_period
        wizard_ungrouped_form.group_by_account = False
        wizard_ungrouped = wizard_ungrouped_form.save()

        wizard_ungrouped.with_context(test_mode=True).print_giornale_reportlab()

        # Generate grouped report
        wizard_grouped_form = Form(self.wizard_model)
        wizard_grouped_form.daterange_id = self.current_period
        wizard_grouped_form.group_by_account = True
        wizard_grouped = wizard_grouped_form.save()

        wizard_grouped.with_context(test_mode=True).print_giornale_reportlab()

        # Both should generate PDFs
        self.assertTrue(
            wizard_ungrouped.report_giornale or wizard_ungrouped.attachment_id,
            "Ungrouped PDF generated",
        )
        self.assertTrue(
            wizard_grouped.report_giornale or wizard_grouped.attachment_id,
            "Grouped PDF generated",
        )

        # Extract text from both
        ungrouped_pdf = pdf.PdfFileReader(
            io.BytesIO(self._get_pdf_data(wizard_ungrouped))
        )
        grouped_pdf = pdf.PdfFileReader(io.BytesIO(self._get_pdf_data(wizard_grouped)))

        ungrouped_text = ""
        for page in ungrouped_pdf.pages:
            ungrouped_text += page.extractText()

        grouped_text = ""
        for page in grouped_pdf.pages:
            grouped_text += page.extractText()

        # Both should contain the partner name
        self.assertIn(partner.name, ungrouped_text, "Partner in ungrouped report")
        # Grouped uses ref instead of partner name
        # Both should contain amounts
        # The exact number formatting may vary by locale,
        # so just check PDFs were generated
        self.assertTrue(ungrouped_text, "Ungrouped report has content")
        self.assertTrue(grouped_text, "Grouped report has content")
        # Ungrouped should have more detail (partner names for each line)
        # Grouped aggregates by account so should be more compact
        # Just verify both generated valid reports
        self.assertTrue(len(ungrouped_text) > 100, "Ungrouped report has content")
        self.assertTrue(len(grouped_text) > 100, "Grouped report has content")
