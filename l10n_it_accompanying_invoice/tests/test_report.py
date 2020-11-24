# Copyright 2020 Simone Vanin - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import odoo.tests


class TestReport(odoo.tests.TransactionCase):
    def test_report(self):
        report = self.env['ir.actions.report']._get_report_from_name(
            'l10n_it_accompanying_invoice.accompanying_invoice_template'
        )

        partner1 = self.env.ref('base.res_partner_1')
        invoice = self.env['account.invoice'].create({
            'partner_id': partner1.id
        })

        html = report.render_qweb_html([invoice.id])

        self.assertTrue(html)
