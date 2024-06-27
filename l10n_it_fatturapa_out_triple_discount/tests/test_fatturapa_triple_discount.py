# Copyright 2019 Simone Rubino - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo.tests import Form, tagged

from .fatturapa_common import Common


@tagged("post_install", "-at_install")
class TestEInvoiceTripleDiscount(Common):
    def test_xml_export_triple_discount(self):
        partner = self.res_partner_fatturapa_0
        partner.vat = "IT00146089990"
        partner.fiscalcode = "00146089990"
        invoice = self.init_invoice(
            "out_invoice",
            invoice_date="2016-01-07",
            partner=partner,
            products=self.product_product_10,
            taxes=self.tax_22,
        )
        invoice_form = Form(invoice)
        invoice_form.invoice_payment_term_id = self.account_payment_term
        with invoice_form.invoice_line_ids.edit(0) as line:
            line.name = "Mouse\nOptical"
            line.price_unit = 10
            line.discount = 50
            line.discount2 = 50
            line.discount3 = 50
        invoice = invoice_form.save()
        invoice.action_post()
        res = self.run_wizard(invoice.id)

        self.assertTrue(res)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        xml_tree = self.get_xml_tree_from_string(xml_content)
        expected_xml = self.getFile("IT06363391001_00001.xml")[1]
        expected_xml_content = base64.decodebytes(expected_xml)
        expected_xml_tree = self.get_xml_tree_from_string(expected_xml_content)
        self.assertXmlTreeEqual(
            xml_tree,
            expected_xml_tree,
        )
