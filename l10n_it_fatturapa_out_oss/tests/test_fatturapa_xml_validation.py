# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import fields
from odoo.tests import Form, tagged

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestInvoiceOss(FatturaPACommon):
    def setUp(self):
        super().setUp()

        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = False
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

        self.product_product_10.write({"taxes_id": [(6, 0, self.tax_22.ids)]})

        tax1_form = Form(self.env["account.tax"])
        tax1_form.name = "OSS AU"
        tax1_form.amount = 20.0
        tax1_form.kind_id = self.env.ref("l10n_it_account_tax_kind.n3_2")
        tax1_form.law_reference = "NON IMPONIBILE ART. 41 COMMA 1, LETT. B"
        self.tax1 = tax1_form.save()
        self.tax1.oss_country_id = self.env.ref("base.at").id

        fp_form = Form(self.env["account.fiscal.position"])
        fp_form.name = "OSS Test"
        with fp_form.tax_ids.new() as tax_form:
            tax_form.tax_src_id = self.tax_22
            tax_form.tax_dest_id = self.tax1
        self.fiscal_position = fp_form.save()

        self.eu_b2c_customer = self.env["res.partner"].create(
            {
                "name": "EU B2C Customer",
                "customer_rank": 1,
                "is_company": False,
                "street": "11 Wien St",
                "is_pa": False,
                "city": "Wolfsgraben",
                "zip": "12345",
                "country_id": self.env.ref("base.at").id,
                "codice_destinatario": "XXXXXXX",
            }
        )

    def _create_invoice(self, date):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.invoice_date = fields.Date.from_string(date)
        move_form.partner_id = self.eu_b2c_customer
        move_form.invoice_payment_term_id = self.env.ref(
            "account.account_payment_term_end_following_month"
        )
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.quantity = 1
            line_form.product_uom_id = self.product_uom_unit
            line_form.price_unit = 14.0
            line_form.account_id = self.a_sale
            line_form.tax_ids.add(self.tax_22)
        account_move = move_form.save()
        return account_move

    def test_1_oss_xml_export(self):
        date = "2022-02-28"
        invoice = self._create_invoice(date)
        move_form = Form(invoice)
        move_form.fiscal_position_id = self.fiscal_position
        with move_form.invoice_line_ids.edit(0) as line_form:
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax1)
        invoice = move_form.save()
        self.assertEqual(
            fields.first(invoice.invoice_line_ids).tax_ids[:1].name,
            self.tax1.name,
        )
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")

    def test_2_oss_xml_export(self):
        date = "2023-02-28"
        invoice = self._create_invoice(date)
        self.assertEqual(
            fields.first(invoice.invoice_line_ids).tax_ids[:1].name,
            self.tax_22.name,
        )
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00002.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00002.xml")
