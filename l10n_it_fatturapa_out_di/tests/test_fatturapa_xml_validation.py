# Copyright 2021 Marco Colombo https://github.com/TheMule71

import base64

from odoo import fields
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (FatturaPACommon)


class TestInvoiceDI(FatturaPACommon):
    def setUp(self):
        super(TestInvoiceDI, self).setUp()

        self.today_date = fields.Date.today()

        self.tax1 = self.env["account.tax"].create({
            "name": "FC INC",
            "amount": 0,
            "price_include": True,
            "kind_id": self.env.ref("l10n_it_account_tax_kind.n3_5").id,
            "law_reference": "Art. 8 co. 1 lett. c) e co. 2 del DPR 633/72",

        })

        self.fiscal_position = self.env["account.fiscal.position"].sudo().create({
            "name": "Dichiarazione Test",
            "valid_for_dichiarazione_intento": True,
            "tax_ids": [(0, 0, {
                "tax_src_id": self.tax_22.id,
                "tax_dest_id": self.tax1.id,
            })]
        })

        self.account = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_receivable').id)
        ], limit=1)

        self.env['dichiarazione.intento.yearly.limit'].create({
            'year': '2016',
            'limit_amount': 50000.0,
            'company_id': self.env.user.company_id.id,
        })

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out_di'
        return super(TestInvoiceDI, self).getAttachment(name, module_name)

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out_di'
        return super(TestInvoiceDI, self).getFile(filename, module_name)

    def _create_dichiarazione(self):
        return self.env['dichiarazione.intento'].sudo().create({
            'partner_id': self.res_partner_fatturapa_0.id,
            'date': fields.Date.from_string("2016-06-15"),
            'date_start': fields.Date.from_string("2016-06-15"),
            'date_end': self.today_date.strftime('%Y-%m-%d'),
            'taxes_ids': [(6, 0, [self.tax1.id])],
            'limit_amount': 1000.00,
            'fiscal_position_id': self.fiscal_position.id,
            'type': 'out',
            'telematic_protocol': '08060120341234567-000001',
            "partner_document_number": "DI/111",
            "partner_document_date": fields.Date.from_string("2016-06-15"),

        })

    def _create_invoice(self):
        payment_term = self.env.ref('account.account_payment_term')
        return self.env["account.invoice"].create({
            "name": "Test Invoice for Dichiarazione",
            "type": "out_invoice",
            "account_id": self.account.id,
            "date_invoice": fields.Date.from_string("2016-06-15"),
            "partner_id": self.res_partner_fatturapa_0.id,
            "fiscal_position_id": self.fiscal_position.id,
            "payment_term_id": payment_term.id,
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.product_product_10.name,
                    "product_id": self.product_product_10.id,
                    "quantity": 1,
                    "uom_id": self.product_uom_unit.id,
                    "price_unit": 14,
                    "account_id": self.a_sale.id,
                    "invoice_line_tax_ids": [(6, 0, [self.tax1.id, ])],
                })
            ],
        })

    def test_1_di_xml_export(self):
        dec = self._create_dichiarazione()

        self.set_sequences(1, "2016-06-15")
        invoice = self._create_invoice()
        invoice.dichiarazione_intento_ids = [(6, 0, [dec.id])]
        invoice.invoice_line_ids.filtered("product_id")[0]\
            .force_dichiarazione_intento_id = dec.id
        invoice.action_invoice_open()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")

    def test_2_di_xml_export(self):
        dec = self._create_dichiarazione()

        self.set_sequences(1, "2016-06-15")
        invoice = self._create_invoice()
        invoice.dichiarazione_intento_ids = [(6, 0, [dec.id])]
        invoice.action_invoice_open()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00002.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00002.xml")

    def test_3_di_xml_export(self):
        dec2 = self._create_dichiarazione()
        dec2.telematic_protocol = '08060120341234567-000002'
        dec2.partner_document_number = "DI/112"

        dec1 = self._create_dichiarazione()

        self.set_sequences(1, "2016-06-15")
        invoice = self._create_invoice()
        invoice.dichiarazione_intento_ids = [(6, 0, [dec1.id, dec2.id, ])]
        invoice.invoice_line_ids.filtered("product_id")[0]\
            .force_dichiarazione_intento_id = dec2.id
        invoice.action_invoice_open()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00003.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00003.xml")
