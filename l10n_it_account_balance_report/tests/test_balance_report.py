#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import tests
from odoo.tests import Form


class TestBalanceReport (tests.SavepointCase):

    @classmethod
    def _create_invoice(cls, partner, products=None, post=False):
        """Get an invoice for `partner`, containing `products`.

        If `post`, the invoice is opened.
        """
        if products is None:
            products = cls.env['product.product'].browse()

        invoice_form = Form(cls.env['account.invoice'])
        invoice_form.partner_id = partner
        for product in products:
            with invoice_form.invoice_line_ids.new() as line:
                line.product_id = product
        invoice = invoice_form.save()

        if post:
            invoice.action_invoice_open()
        return invoice

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': "Test Customer",
            'customer': True,
        })

        cls.product = cls.env['product.product'].create({
            'name': "Test Product",
        })

        cls.posted_invoice = cls._create_invoice(
            cls.customer,
            products=cls.product,
            post=True,
        )

    def _get_report_content(self, wizard_values):
        """Get the PDF content from the wizard created with `wizard_values`."""
        # Get the Report Action from the Wizard
        wiz = self.env['trial.balance.report.wizard'].create(wizard_values)
        report_action = wiz.button_export_pdf()

        # Get the Report from the Report Action
        report_name = report_action['report_name']
        context = report_action['context']
        report_ids = context['active_ids']
        report = self.env['ir.actions.report']._get_report_from_name(report_name)

        # Render the Report
        report_content, report_type = report \
            .with_context(context) \
            .render_qweb_pdf(report_ids)
        report_content = report_content.decode()
        return report_content

    def test_hide_accounts_codes(self):
        """The Account Code is hidden
        when `hide_accounts_codes` is enabled.
        """
        # Arrange
        invoice = self.posted_invoice
        account = invoice.invoice_line_ids.account_id
        # pre-condition: An Invoice is posted
        self.assertEqual(invoice.state, 'open')

        # Act: Print the Report containing the Invoice,
        # enabling `hide_accounts_codes`
        one_day = timedelta(days=1)
        report_content = self._get_report_content({
            'account_balance_report_type': 'profit_loss',
            'hide_accounts_codes': True,
            'date_from': invoice.date_invoice - one_day,
            'date_to': invoice.date_invoice + one_day,
        })

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
        self.assertEqual(invoice.state, 'open')

        # Act: Print the Report containing the Invoice
        one_day = timedelta(days=1)
        report_content = self._get_report_content({
            'account_balance_report_type': 'profit_loss',
            'date_from': invoice.date_invoice - one_day,
            'date_to': invoice.date_invoice + one_day,
        })

        # Assert: The Account Code is shown
        self.assertIn(account.code, report_content)
        self.assertIn(account.name, report_content)
