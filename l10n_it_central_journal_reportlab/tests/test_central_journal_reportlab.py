# Copyright 2022 Giuseppe Borruso
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
        self.range_type = self.env["date.range.type"].create({"name": "Fiscal year"})
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
