# Copyright 2020 Simone Vanin - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestReport(AccountTestInvoicingCommon):
    def test_report(self):
        invoice = self.init_invoice(
            "out_invoice",
        )

        report = self.env["ir.actions.report"]._get_report_from_name(
            "l10n_it_accompanying_invoice.shipping_invoice_template"
        )
        html = report._render_qweb_html(invoice.id)
        self.assertTrue(html)
