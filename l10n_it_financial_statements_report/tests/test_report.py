#  Copyright 2023 Simone Rubino - TAKOBI
#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

import xlrd

from odoo import tests
from odoo.tools.safe_eval import safe_eval

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tests.tagged("post_install", "-at_install")
class TestReport(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test Customer",
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )

        cls.posted_invoice = cls.init_invoice(
            "out_invoice",
            partner=cls.customer,
            products=cls.product,
            post=True,
        )

        account = cls.posted_invoice.invoice_line_ids.account_id
        # Do not use entire account code, so it does not cause false positives
        # when looking for the account code in the reports
        group_code = account.code[:-1]
        cls.account_group = cls.env["account.group"].create(
            {
                "name": "Test Group",
                "code_prefix_start": group_code,
                "code_prefix_end": group_code,
            }
        )

    def _get_report_action(self, wizard_values, report_type):
        wizard_action = self.env.ref(
            "l10n_it_financial_statements_report.action_financial_statements_wizard"
        )
        wizard_model = wizard_action.res_model
        wizard_context = safe_eval(wizard_action.context) or dict()

        wiz = (
            self.env[wizard_model]
            .with_context(
                discard_logo_check=True,
                **wizard_context,
            )
            .create(wizard_values)
        )
        if report_type == "pdf":
            report_action = wiz.button_export_pdf()
        elif report_type == "xlsx":
            report_action = wiz.button_export_xlsx()
        else:
            raise Exception(f"Report Type {report_type} not supported")
        return report_action

    def _render_report(self, report, report_data, report_type, wizard_ids):
        if report_type == "pdf":
            report_content, report_type = report._render_qweb_pdf(
                report,
                res_ids=wizard_ids,
                data=report_data,
            )
            report_content = report_content.decode()
        elif report_type == "xlsx":
            report_content, report_type = report._render_xlsx(
                report,
                wizard_ids,
                report_data,
            )
        else:
            raise Exception(f"Report Type {report_type} not supported")
        return report_content

    def _get_report_content(self, wizard_values, report_type="pdf"):
        """Get the PDF content from the wizard created with `wizard_values`."""
        report_action = self._get_report_action(wizard_values, report_type)

        # Get the Report from the Report Action
        report_name = report_action["report_name"]
        context = report_action["context"]
        wizard_ids = context["active_ids"]
        report = self.env["ir.actions.report"]._get_report_from_name(report_name)
        report = report.with_context(**context)
        report_data = report_action["data"]

        report_content = self._render_report(
            report, report_data, report_type, wizard_ids
        )

        return report_content

    def test_hide_accounts_codes(self):
        """The Account Code is hidden
        when `hide_accounts_codes` is enabled.
        """
        # Arrange
        invoice = self.posted_invoice
        account = invoice.invoice_line_ids.account_id
        # pre-condition: An Invoice is posted
        self.assertEqual(invoice.state, "posted")

        # Act: Print the Report containing the Invoice,
        # enabling `hide_accounts_codes`
        one_day = timedelta(days=1)
        report_content = self._get_report_content(
            {
                "financial_statements_report_type": "profit_loss",
                "hide_accounts_codes": True,
                "date_from": invoice.invoice_date - one_day,
                "date_to": invoice.invoice_date + one_day,
            }
        )

        # Assert: The Account Code is hidden
        self.assertNotIn(account.code, report_content)
        self.assertIn(account.name, report_content)

    def test_show_accounts_codes(self):
        """The Account Code is shown
        when `hide_accounts_codes` is disabled (default value).
        """
        # Arrange
        invoice = self.posted_invoice
        account = invoice.invoice_line_ids.account_id
        # pre-condition: An Invoice is posted
        self.assertEqual(invoice.state, "posted")

        # Act: Print the Report containing the Invoice
        one_day = timedelta(days=1)
        report_content = self._get_report_content(
            {
                "financial_statements_report_type": "profit_loss",
                "date_from": invoice.invoice_date - one_day,
                "date_to": invoice.invoice_date + one_day,
            }
        )

        # Assert: The Account Code is shown
        self.assertIn(account.code, report_content)
        self.assertIn(account.name, report_content)

    def test_xlsx(self):
        # Arrange
        invoice = self.posted_invoice
        # pre-condition: An Invoice is posted
        self.assertEqual(invoice.state, "posted")

        # Act: Print the XLSX Report containing the Invoice
        one_day = timedelta(days=1)
        report_content = self._get_report_content(
            {
                "financial_statements_report_type": "profit_loss",
                "date_from": invoice.invoice_date - one_day,
                "date_to": invoice.invoice_date + one_day,
            },
            report_type="xlsx",
        )
        workbook = xlrd.open_workbook(file_contents=report_content)
        sheet = workbook.sheet_by_index(0)

        # Assert
        account_group = self.account_group
        code_column_index, name_column_index, amount_column_index = 3, 4, 5
        # Group line
        group_row_index = 11
        self.assertEqual(
            sheet.cell(group_row_index, code_column_index).value,
            account_group.complete_code,
        )
        self.assertEqual(
            sheet.cell(group_row_index, name_column_index).value, account_group.name
        )
        self.assertEqual(
            sheet.cell(group_row_index, amount_column_index).value,
            invoice.amount_untaxed,
        )
        # Account line
        account_row_index = 12
        account = invoice.invoice_line_ids.account_id
        self.assertEqual(account_group, account.group_id)
        self.assertEqual(
            sheet.cell(account_row_index, code_column_index).value, account.code
        )
        self.assertEqual(
            sheet.cell(account_row_index, name_column_index).value, account.name
        )
        self.assertEqual(
            sheet.cell(account_row_index, amount_column_index).value,
            invoice.amount_untaxed,
        )
        # Totals line
        totals_row_index = 14
        account = invoice.invoice_line_ids.account_id
        self.assertEqual(account_group, account.group_id)
        total_string = sheet.cell(totals_row_index, code_column_index).value
        self.assertIn(str(invoice.amount_untaxed), total_string)
