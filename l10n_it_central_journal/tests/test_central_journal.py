# Copyright 2017 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime

from dateutil.rrule import MONTHLY
from lxml import html

from odoo.tests.common import Form, TransactionCase


class TestCentralJournal(TransactionCase):
    def setUp(self):
        super(TestCentralJournal, self).setUp()

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
        self.wizard_model = self.env["wizard.giornale"]
        self.report_model = self.env["ir.actions.report"]
        self.report_name = "l10n_it_central_journal.report_giornale"
        self.journals = self.env["account.journal"].search([])

    def test_wizard(self):
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

        report_data = wizard.print_giornale()
        html_data = self.report_model._get_report_from_name(
            self.report_name
        )._render_qweb_html(wizard, report_data["context"]["report_action"]["data"])[0]
        content = html.document_fromstring(html_data)

        text_content = content.xpath("//span[@id='l10n_it_count_fiscal_page_base']")[
            0
        ].text_content()

        self.assertEqual(text_content, str(wizard.fiscal_page_base))
