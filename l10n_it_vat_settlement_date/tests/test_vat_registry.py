#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo import Command
from odoo.tests import Form, tagged
from odoo.tools import format_date

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestVATRegistry(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.supplier_bill = cls.init_invoice(
            "in_invoice",
            invoice_date=datetime.date(2020, 6, 15),
            amounts=[
                100,
            ],
            post=True,
        )
        cls.supplier_journal = cls.company_data["default_journal_purchase"]
        cls.supplier_tax_registry = cls.env["account.tax.registry"].create(
            {
                "name": "Supplier",
                "layout_type": "supplier",
                "journal_ids": [
                    Command.set(cls.supplier_journal.ids),
                ],
            }
        )

    def _get_wizard(self, from_date, to_date, tax_registry):
        """Create the wizard to print the VAT Registry."""
        wizard_form = Form(self.env["wizard.registro.iva"])
        wizard_form.from_date = from_date
        wizard_form.to_date = to_date
        wizard_form.tax_registry_id = tax_registry
        wizard = wizard_form.save()
        return wizard

    def _get_report(self, from_date, to_date, tax_registry):
        """Print the VAT Registry."""
        wizard = self._get_wizard(from_date, to_date, tax_registry)

        report_action = wizard.with_context(discard_logo_check=True).print_registro()
        report_name = report_action["report_name"]
        report_context = report_action["context"]
        report_data = report_action["data"]
        html, _report_type = (
            self.env["ir.actions.report"]
            .with_context(**report_context)
            ._render_qweb_html(report_name, wizard.ids, data=report_data)
        )
        return html

    def test_report(self):
        """The settlement date is shown in the report."""
        # Arrange: a date range and a bill in that range
        bill = self.supplier_bill
        accounting_date = bill.date
        settlement_date = bill.date + relativedelta(years=1)
        bill.l10n_it_vat_settlement_date = settlement_date
        tax_registry = self.supplier_tax_registry
        from_date = datetime.date(2020, 1, 1)
        to_date = datetime.date(2020, 12, 31)
        # pre-condition: the report contains the bill
        self.assertTrue(from_date <= accounting_date <= to_date)
        self.assertNotEqual(accounting_date, settlement_date)

        # Act
        html = self._get_report(
            from_date,
            to_date,
            tax_registry,
        )

        # Assert
        report_content = html.decode()
        self.assertIn(bill.name, report_content)
        self.assertIn(format_date(self.env, settlement_date), report_content)
