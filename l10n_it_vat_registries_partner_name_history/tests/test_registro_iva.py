#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
import json
import operator
from functools import reduce

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.partner_name_history.tests.common import (
    _get_name_from_date,
    _set_partner_name,
)


@tagged("post_install", "-at_install")
class TestVATRegistry(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.sale_tax_registry = cls.env["account.tax.registry"].create(
            {
                "name": "Sales",
                "layout_type": "customer",
                "journal_ids": cls.company_data["default_journal_sale"].ids,
            }
        )

    def _get_report_content(self, from_date, to_date, tax_registry):
        wizard_form = Form(self.env["wizard.registro.iva"])
        wizard_form.from_date = from_date
        wizard_form.to_date = to_date
        wizard_form.tax_registry_id = tax_registry
        wizard = wizard_form.save()
        res = wizard.with_context(
            discard_logo_check=True,
        ).print_registro()

        report_name = res["report_name"]
        report_context = json.loads(res["data"]["context"])
        report_action = self.env["ir.actions.report"].search(
            [
                ("report_type", "=", res["report_type"]),
                ("report_name", "=", report_name),
            ]
        )
        data = res["data"]
        content, _type = report_action.with_context(**report_context)._render_qweb_html(
            report_name, data["ids"], data
        )
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

        # Act
        content = self._get_report_content(
            min(invoice_dates),
            max(invoice_dates),
            self.sale_tax_registry,
        )

        # Assert
        content = content.decode()
        last_partner_name = partner.name
        self.assertIn(original_partner_name, content)
        self.assertIn(_get_name_from_date(change_dates[0]), content)
        self.assertIn(last_partner_name, content)
