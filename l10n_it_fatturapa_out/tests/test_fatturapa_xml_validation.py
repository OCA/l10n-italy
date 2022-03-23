# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Alex Comba - Agile Business Group

import base64
import re

from psycopg2 import IntegrityError

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tools import mute_logger

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestDuplicatedAttachment(FatturaPACommon):
    def test_duplicated_attachment(self):
        """Attachment name must be unique"""
        # This test breaks the current transaction
        # and every test executed after this in the
        # same transaction would fail.
        # Note that all the tests in TestFatturaPAXMLValidation
        # are executed in the same transaction.
        # name and att_name are both needed
        self.attach_model.create(
            {"name": "test_duplicated", "att_name": "test_duplicated"}
        )
        with self.assertRaises(IntegrityError) as ie:
            with mute_logger("odoo.sql_db"):
                self.attach_model.create(
                    {"name": "test_duplicated", "att_name": "test_duplicated"}
                )
        self.assertEqual(ie.exception.pgcode, "23505")


@tagged("post_install", "-at_install")
class TestFatturaPAXMLValidation(FatturaPACommon):
    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.company = self.env.company = self.sales_journal.company_id

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
        # self.env.user.company_ids = self.env.user.company_ids[1]
        # self.env.user.company_id = self.env.company

    def test_1_xml_export(self):
        self.env.company.fatturapa_pub_administration_ref = "F000000111"
        self.set_sequences(13, "2016-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0013",
                "company_id": self.env.company.id,
                "invoice_date": "2016-01-07",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse\nOptical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        self.assertFalse(self.attach_model.file_name_exists("00001"))
        res = self.run_wizard(invoice.id)

        self.assertTrue(res)
        attachment = self.attach_model.browse(res["res_id"])
        file_name_match = "^%s_[A-Za-z0-9]{5}.xml$" % self.env.company.vat
        # Checking file name randomly generated
        self.assertTrue(re.search(file_name_match, attachment.name))
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        self.assertTrue(self.attach_model.file_name_exists("00001"))

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")

    def test_2_xml_export(self):
        self.set_sequences(14, "2016-06-15")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0014",
                "invoice_date": "2016-06-15",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "narration": "prima riga\nseconda riga",
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
                "related_documents": [
                    (
                        0,
                        0,
                        {
                            "type": "order",
                            "name": "PO123",
                            "cig": "123",
                            "cup": "456",
                        },
                    )
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00002.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00002.xml")

    def test_3_xml_export(self):
        self.set_sequences(15, "2016-06-15")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0015",
                "invoice_date": "2016-06-15",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "narration": "prima riga\nseconda riga",
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
                            "admin_ref": "D122353",
                            "tax_ids": [(6, 0, {self.tax_22.id})],
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
                "related_documents": [
                    (
                        0,
                        0,
                        {
                            "type": "order",
                            "name": "PO123",
                            "cig": "123",
                            "cup": "456",
                        },
                    )
                ],
            }
        )
        invoice._post()
        self.AttachFileToInvoice(invoice.id, "test1.pdf")
        self.AttachFileToInvoice(invoice.id, "test2.pdf")
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00003.xml")
        xml_content = base64.decodebytes(attachment.datas)

        self.check_content(xml_content, "IT06363391001_00003.xml")

    def test_5_xml_export(self):
        self.env.company.fatturapa_sender_partner = self.intermediario.id
        self.set_sequences(17, "2016-06-15")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0017",
                "invoice_date": "2016-06-15",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
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
                            "discount": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT03297040366_00005.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT03297040366_00005.xml")

    def test_6_xml_export(self):
        self.product_product_10.default_code = "ODOOCODE"
        self.product_order_01.barcode = "987654"
        self.set_sequences(13, "2018-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2018/0013",
                "invoice_date": "2018-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00006.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00006.xml")

    def test_7_xml_export(self):
        self.product_product_10.default_code = False
        self.product_order_01.barcode = False
        self.company.partner_id.vat = "CHE-114.993.395 IVA"
        self.company.partner_id.name = "Azienda estera"
        self.company.partner_id.city = "Lugano"
        self.company.partner_id.state_id = False
        self.company.partner_id.country_id = self.env.ref("base.ch").id
        self.company.fatturapa_tax_representative = self.intermediario.id
        self.company.fatturapa_stabile_organizzazione = self.stabile_organizzazione.id
        self.set_sequences(14, "2018-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2018/0014",
                "invoice_date": "2018-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "CHE114993395IVA_00007.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "CHE114993395IVA_00007.xml")

    def test_8_xml_export(self):
        self.tax_22.price_include = True
        self.set_sequences(15, "2018-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2018/0015",
                "invoice_date": "2018-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "narration": "firsrt line\n\nsecond line",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
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
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00008.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00008.xml")

    def test_10_xml_export(self):
        # invoice with descriptive line
        self.set_sequences(10, "2019-08-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2019/0010",
                "invoice_date": "2019-08-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                # "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse\nOptical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_10.id})],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "display_type": "line_note",
                            "name": "Notes",
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                            "currency_id": self.EUR.id,
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00010.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00010.xml")

    def test_11_xml_export(self):
        self.set_sequences(11, "2018-01-07")
        self.product_product_10.default_code = "GH82Ø23€ŦD11"
        self.product_order_01.default_code = "GZD11"
        partner = self.res_partner_fatturapa_2
        partner.name = "REMODELAÇÃO DECORAÇÃO ŽALEC LDAŠ"
        partner.street = "Mžaja ŠtraÇÃ 14"
        partner.zip = "ES-49714"
        partner.city = "Šofıa"
        partner.country_id = self.env.ref("base.si").id
        partner.vat = "SI12345679"
        partner.fiscalcode = False
        partner.onchange_country_id_e_inv()
        partner.write(partner._convert_to_write(partner._cache))
        self.assertEqual(partner.codice_destinatario, "XXXXXXX")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2018/0011",
                "invoice_date": "2018-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical Ø23 ß11",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_order_01.id,
                            "name": "Zed+^ Antiv° (£)",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 4,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )

        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00011.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00011.xml")

    def test_12_xml_export(self):
        invoicing_partner = self.env["res.partner"].create(
            {
                "parent_id": self.res_partner_fatturapa_2.id,
                "type": "invoice",
                "city": "Sanremo",
                "zip": "18038",
                "country_id": self.env.ref("base.it").id,
                "state_id": self.env.ref("base.state_us_2").id,
                "street": "Via Roma, 1",
                "codice_destinatario": "0000000",
                "pec_destinatario": "test_invoice@pec.it",
                "electronic_invoice_use_this_address": True,
            }
        )
        self.set_sequences(12, "2020-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2020/0012",
                "invoice_date": "2020-01-07",
                "partner_id": invoicing_partner.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    )
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00012.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00012.xml")

    def test_13_xml_export(self):
        self.set_sequences(13, "2020-01-07")
        self.tax_00_ns.kind_id = self.env.ref("l10n_it_account_tax_kind.n2_1")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2020/0013",
                "invoice_date": "2020-01-07",
                "partner_id": self.res_partner_fatturapa_5.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_00_ns.id})],
                        },
                    )
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00013.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00013.xml")

    def test_14_xml_export(self):
        """
        - create two product lines with different taxes, but same tax amount

        expect two <DatiRiepilogo> entries
        """

        product_product_9 = self.env.ref("product.product_product_9")
        tax_22b = self.tax_22.copy({"name": self.tax_22.name + "b"})

        invoice_form = Form(
            self.env["account.move"].with_context({"default_move_type": "out_invoice"})
        )
        invoice_form.partner_id = self.res_partner_fatturapa_0
        invoice_form.name = "INV/2021/10/0001"
        invoice_form.date = fields.Date.from_string("2021-10-29")
        invoice_form.invoice_date = fields.Date.from_string("2021-10-29")
        with invoice_form.line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_22)
        with invoice_form.line_ids.new() as line_form:
            line_form.product_id = product_product_9
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(tax_22b)
        invoice = invoice_form.save()
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00014.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00014.xml")

    def test_15_xml_export(self):
        """
        - create an invoice in USD

        expect an XML with values in EUR
        """

        usd = self.env.ref("base.USD")

        self.env["res.currency.rate"].create(
            {
                "name": fields.Date.from_string("2021-12-16"),
                "rate": 1.17,
                "currency_id": usd.id,
                "company_id": self.env.company.id,
            }
        )

        invoice_form = Form(
            self.env["account.move"].with_context({"default_move_type": "out_invoice"})
        )
        invoice_form.currency_id = usd
        invoice_form.partner_id = self.res_partner_fatturapa_0
        invoice_form.name = "INV/2021/12/0001"
        invoice_form.date = fields.Date.from_string("2021-12-16")
        invoice_form.invoice_date = fields.Date.from_string("2021-12-16")
        invoice_form.invoice_payment_term_id = self.account_payment_term

        self.tax_00_ns.kind_id = self.env.ref("l10n_it_account_tax_kind.n3_2")

        with invoice_form.line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_00_ns)
        invoice = invoice_form.save()
        invoice.action_post()

        # commit 86febae278f08864e83017d43f6aa9d67165d664 fixed this as
        # a side effect: now the price is actually 14.00 USD not 16.38
        # for env.ref("product.product_product_10")
        # self.assertEqual(invoice.invoice_line_ids[0].price_unit, 16.38)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 14.00)

        invoice.company_id.xml_divisa_value = "force_eur"
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00015.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00015.xml")
        attachment.unlink()

        invoice.company_id.xml_divisa_value = "keep_orig"
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00016.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00016.xml")

    def test_no_tax_fail(self):
        """
        - create an invoice with a product line without taxes

        expect to fail with a proper message
        """
        invoice_form = Form(
            self.env["account.move"].with_context({"default_move_type": "out_invoice"})
        )
        invoice_form.partner_id = self.res_partner_fatturapa_0
        with invoice_form.line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
        with invoice_form.line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = invoice_form.save()
        invoice.action_post()

        wizard = self.wizard_model.create({})
        with self.assertRaises(UserError) as ue:
            wizard.with_context({"active_ids": [invoice.id]}).exportFatturaPA()
        error_message = "Invoice {} contains product lines w/o taxes".format(
            invoice.name
        )
        self.assertEqual(ue.exception.args[0], error_message)

    def test_multicompany_fail(self):
        """
        - create two invoices in two different companies
        - try and export both invoices in one single XML file

        expect to fail with a proper message
        """

        invoice1_form = Form(
            self.env["account.move"].with_context({"default_move_type": "out_invoice"})
        )
        invoice1_form.partner_id = self.res_partner_fatturapa_0
        with invoice1_form.line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_22)
        invoice1 = invoice1_form.save()

        company_form = Form(self.env["res.company"].sudo(True))
        company_form.name = "YourCompany 2"
        company_form.vat = "IT07973780013"
        company_form.fatturapa_fiscal_position_id = (
            self.env.company.fatturapa_fiscal_position_id
        )
        company2 = company_form.save()

        self.env.user.company_ids |= company2

        journal2 = invoice1.journal_id.copy()
        journal2.write(
            {
                "company_id": company2.id,
            }
        )
        invoice2 = invoice1.copy()
        invoice2.write(
            {
                "name": invoice1.name,
                "company_id": company2.id,
                "journal_id": journal2.id,
            }
        )

        self.assertTrue(company2 != self.env.company)
        self.assertEqual(invoice1.company_id, self.env.company)
        self.assertEqual(invoice2.company_id, company2)
        invoice1.action_post()
        invoice2.action_post()
        wizard = self.wizard_model.create({})
        with self.assertRaises(UserError) as ue:
            wizard.with_context(
                {"active_ids": [invoice1.id, invoice2.id]}
            ).exportFatturaPA()
        error_message = "Invoices {}, {} must belong to the same company.".format(
            invoice1.name, invoice2.name
        )
        self.assertEqual(ue.exception.args[0], error_message)

    def test_unlink(self):
        e_invoice = self._create_e_invoice()
        e_invoice.unlink()
        self.assertFalse(e_invoice.exists())

    def test_reset_to_ready(self):
        e_invoice = self._create_e_invoice()
        e_invoice.state = "sender_error"
        e_invoice.reset_to_ready()
        self.assertEqual(e_invoice.state, "ready")

    def test_no_export_bill(self):
        invoice = self.invoice_model.create(
            {
                "partner_id": self.res_partner_fatturapa_0.id,
                "invoice_date": "2020-01-07",
                "user_id": self.user_demo.id,
                "move_type": "in_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": "Mouse Optical",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    )
                ],
            }
        )
        invoice._post()
        with self.assertRaises(UserError) as ue:
            self.run_wizard(invoice.id)
        self.assertIn(invoice.name, ue.exception.args[0])

    def test_trasmittente_xml_export(self):
        self.env.company.e_invoice_transmitter_id = self.trasmittente.id
        self.set_sequences(19, "2022-03-23")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2022/0019",
                "invoice_date": "2022-03-23",
                "partner_id": self.res_partner_fatturapa_0.id,
                "journal_id": self.sales_journal.id,
                # "account_id": self.a_recv.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
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
                            "discount": 10,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )
        invoice._post()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT03297040366_00019.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT03297040366_00019.xml")
