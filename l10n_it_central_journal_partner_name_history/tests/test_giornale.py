#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import datetime
import io
import operator
from functools import reduce

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, tagged
from odoo.tools import pdf

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.partner_name_history.tests.common import (
    _get_name_from_date,
    _set_partner_name,
)


@tagged("post_install", "-at_install")
class TestCentralJournal(AccountTestInvoicingCommon):
    def _get_report_content(self, date_range):
        wizard_form = Form(self.env["wizard.giornale.reportlab"])
        wizard_form.daterange_id = date_range
        wizard = wizard_form.save()
        wizard.with_context(
            discard_logo_check=True,
        ).print_giornale_reportlab()

        pdf_content = base64.b64decode(wizard.report_giornale)
        pdf_reader = pdf.OdooPdfFileReader(io.BytesIO(pdf_content))
        content = "\n".join([page.extractText() for page in pdf_reader.pages])
        return content

    def test_report(self):
        """The report shows the old name for old invoices."""
        # Arrange
        one_day = relativedelta(days=1)
        partner = self.partner_a
        original_partner_name = partner.name
        change_dates = [
            datetime.date(2019, 1, 1),
            datetime.date(2020, 1, 1),
        ]
        date_to_names = {date: _get_name_from_date(date) for date in change_dates}
        for change_date, name in date_to_names.items():
            _set_partner_name(
                partner,
                name,
                date=change_date,
            )
        moves = reduce(
            operator.ior,
            [
                self.init_invoice(
                    "out_invoice",
                    partner=partner,
                    invoice_date=date,
                    amounts=[
                        100,
                    ],
                    post=True,
                )
                for date in [
                    change_dates[0] - one_day,
                    change_dates[0] + one_day,
                    change_dates[1] - one_day,
                    change_dates[1] + one_day,
                ]
            ],
        )
        invoice_dates = moves.mapped("invoice_date")
        date_range_type_id, _name = self.env["date.range.type"].name_create(
            "Date range type"
        )
        date_range = self.env["date.range"].create(
            {
                "type_id": date_range_type_id,
                "name": "Test date range",
                "date_start": min(invoice_dates),
                "date_end": max(invoice_dates),
            }
        )

        # Act
        content = self._get_report_content(date_range)

        # Assert
        last_partner_name = partner.name
        self.assertIn(original_partner_name, content)
        self.assertIn(_get_name_from_date(change_dates[0]), content)
        self.assertIn(last_partner_name, content)
