#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.tests import Form, tagged

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestXMLGeneration(FatturaPACommon):
    def setUp(self):
        super().setUp()
        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        self.env.company.name = "YourCompany"
        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = True
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.state_id = self.env.ref("base.state_us_2").id
        self.env.company.partner_id.zip = "00100"
        self.env.company.partner_id.phone = "06543534343"
        self.env.company.email = "info@yourcompany.example.com"
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id
        self.env["decimal.precision"].search(
            [("name", "=", "Product Unit of Measure")]
        ).digits = 3
        self.env["uom.uom"].search([("name", "=", "Units")]).name = "Unit(s)"

    def test_fixed_discount(self):
        """Generate an e-invoice for an invoice having a fixed discount.
        Check that the ScontoMaggiorazione is present in the generated e-invoice.
        """
        # Setup for fixing date and sequence of new invoices
        date_invoice = "2020-01-01"
        self.set_sequences(1, date_invoice)

        # Arrange: Create an invoice with one line costing 100
        # and fixed discount of 20
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.res_partner_fatturapa_2
        invoice_form.invoice_date = date_invoice
        with invoice_form.invoice_line_ids.new() as line:
            line.name = "Test fixed discount"
            line.price_unit = 1000
            line.quantity = 1
            line.discount_fixed = 20
            line.account_id = self.a_sale
            line.tax_ids.clear()
            line.tax_ids.add(self.tax_22)
        invoice = invoice_form.save()
        invoice._post()
        # pre-condition: Check invoice totals
        self.assertEqual(invoice.amount_untaxed, 980)
        self.assertEqual(invoice.amount_tax, 215.6)
        self.assertAlmostEqual(invoice.amount_total, 1195.6, 2)

        # Act: Generate the e-invoice
        action = self.run_wizard(invoice.id)
        e_invoice = self.env[action["res_model"]].browse(action["res_id"])

        # Assert: The E-invoice matches the XML in tests data
        file_name = "IT06363391001_00001.xml"
        self.set_e_invoice_file_id(e_invoice, file_name)
        xml_content = base64.decodebytes(e_invoice.datas)
        self.check_content(
            xml_content,
            file_name,
            module_name="l10n_it_fatturapa_out_fd",
        )
