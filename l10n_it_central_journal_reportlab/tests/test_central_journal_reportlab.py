# Copyright 2022 Giuseppe Borruso
# Copyright 2024 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import io
from datetime import datetime

from dateutil.rrule import MONTHLY

from odoo.tests import Form
from odoo.tests.common import TransactionCase
from odoo.tools import pdf


class TestCentralJournalReportlab(TransactionCase):
    def setUp(self):
        super().setUp()

        self.today = datetime.now()
        self.range_type = self.env["date.range.type"].create({"name": "Fiscal year"})
        self.env["date.range.generator"].create(
            {
                "date_start": f"{self.today.year}-01-01",
                "name_prefix": f"{self.today.year}-",
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

        wizard.print_giornale_reportlab()
        decode_giornale = base64.b64decode(wizard.report_giornale)
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
        wizard.print_giornale_reportlab()
        giornale_pdf_content = base64.b64decode(wizard.report_giornale)
        giornale_content = pdf.PdfFileReader(io.BytesIO(giornale_pdf_content))
        has_move = False
        for page in giornale_content.pages:
            page_content = page.extractText()
            if not has_move and out_invoice.name in page_content:
                has_move = True
        self.assertTrue(has_move)
