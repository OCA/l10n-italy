# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Alex Comba - Agile Business Group

import base64

from odoo.tests import tagged

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestFatturaPAXMLValidation(FatturaPACommon):
    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()

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

    def test_4_xml_export(self):
        self.set_sequences(16, "2016-06-15")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0016",
                "invoice_date": "2016-06-15",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "fiscal_position_id": self.fiscal_position_sp.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse, Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22_SP.id})],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_order_01.id,
                            "name": "Zed+ Antivirus",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 4,
                            "tax_ids": [(6, 0, {self.tax_22_SP.id})],
                        },
                    ),
                ],
            }
        )
        self.assertTrue(invoice.fiscal_document_type_id)
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00004.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00004.xml")
