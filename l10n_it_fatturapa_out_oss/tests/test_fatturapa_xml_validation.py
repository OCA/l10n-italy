# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import fields
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (FatturaPACommon)


class TestInvoiceOss(FatturaPACommon):
    def setUp(self):
        super().setUp()

        self.today_date = fields.Date.today()
        self.env.user.company_id.fatturapa_art73 = False
        self.tax1 = self.env["account.tax"].create({
            "name": "OSS AU",
            "amount": 20.0,
            "oss_subjected": True,
            "kind_id": self.env.ref("l10n_it_account_tax_kind.n3_2").id,
            "law_reference": "NON IMPONIBILE ART. 41 COMMA 1, LETT. B",

        })
        self.product_product_10.write({
            "taxes_id": [(6, 0, self.tax_22.ids)]})
        self.fiscal_position = self.env["account.fiscal.position"].sudo().create({
            "name": "OSS Test",
            "tax_ids": [(0, 0, {
                "tax_src_id": self.tax_22.id,
                "tax_dest_id": self.tax1.id,
            })]
        })
        self.account = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable').id)
        ], limit=1)

        self.eu_b2c_customer = self.env['res.partner'].create({
            "name": "EU B2C Customer",
            "customer": True,
            "supplier": False,
            "is_company": False,
            "street": "11 Wien St",
            "is_pa": False,
            "city": "Wolfsgraben",
            "zip": "12345",
            "country_id": self.env.ref("base.at").id,
            "codice_destinatario": "XXXXXXX",
        })

        self.env['oss.year'].create({
            'year': '2022',
            'oss_subjected': True,
            'company_id': self.env.user.company_id.id,
        })
        self.env['oss.year'].create({
            'year': '2023',
            'oss_subjected': False,
            'company_id': self.env.user.company_id.id,
        })

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out_oss'
        return super().getAttachment(name, module_name)

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out_oss'
        return super().getFile(filename, module_name)

    def _create_invoice(self, date):
        payment_term = self.env.ref('account.account_payment_term')
        return self.env["account.invoice"].create({
            "name": "Test Invoice for OSS",
            "type": "out_invoice",
            "account_id": self.account.id,
            "date_invoice": fields.Date.from_string(date),
            "partner_id": self.eu_b2c_customer.id,
            "payment_term_id": payment_term.id,
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.product_product_10.name,
                    "product_id": self.product_product_10.id,
                    "quantity": 1,
                    "uom_id": self.product_uom_unit.id,
                    "price_unit": 14.0,
                    "account_id": self.a_sale.id,
                    "invoice_line_tax_ids": [(6, 0, [self.tax_22.id, ])],
                })
            ],
        })

    def test_1_oss_xml_export(self):
        date = "2022-02-28"
        self.set_sequences(18, date)
        invoice = self._create_invoice(date)
        invoice.fiscal_position_id = self.fiscal_position
        invoice.invoice_line_ids._onchange_product_id()
        invoice.compute_taxes()
        self.assertEqual(invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name,
                         self.tax1.name)
        invoice.action_invoice_open()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")

    def test_2_oss_xml_export(self):
        date = "2023-02-28"
        self.set_sequences(18, date)
        invoice = self._create_invoice(date)
        invoice.invoice_line_ids._onchange_product_id()
        invoice.compute_taxes()
        self.assertEqual(invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name,
                         self.tax_22.name)
        invoice.action_invoice_open()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00002.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00002.xml")
