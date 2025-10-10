# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Alex Comba - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import re
from unittest.mock import Mock

from psycopg2 import IntegrityError

import odoo
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
        super().setUp()
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
                "narration": "first line\n\nsecond line",
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
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.res_partner_fatturapa_0
        invoice_form.invoice_date = fields.Date.from_string("2021-10-29")
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_22)
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = product_product_9
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(tax_22b)
        invoice = invoice_form.save()
        invoice.date = fields.Date.from_string("2021-10-29")
        invoice.name = "INV/2021/10/0001"
        invoice.action_post()
        self._exclude_DatiPagamento(invoice)

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00014.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00014.xml")

    def test_no_payment_term_creates_DatiPagamento(self):
        """When payment_term is not set in the invoice and due date is set,
        DatiPagamento node is created in the e-invoce."""
        # Arrange
        partner = self.res_partner_fatturapa_0
        partner.electronic_invoice_subjected = True
        invoice = self.init_invoice(
            "out_invoice",
            partner=partner,
            invoice_date=fields.Date.from_string("2019-12-31"),
            amounts=[100],
            taxes=self.tax_22,
        )
        with Form(invoice) as invoice_form:
            invoice_form.name = "INV/2019/00100"
            invoice_form.invoice_date_due = fields.Date.from_string("2020-01-01")
            invoice_form.invoice_payment_term_id = self.env[
                "account.payment.term"
            ].browse()
            invoice_form.fatturapa_payment_method_id = self.env[
                "fatturapa.payment_method"
            ].browse()
            invoice_form.fatturapa_payment_term_id = self.env[
                "fatturapa.payment_term"
            ].browse()
        invoice.action_post()
        # pre-condition
        self.assertFalse(invoice.fatturapa_payment_method_id)
        self.assertFalse(invoice.fatturapa_payment_term_id)

        # Act
        # Since payment data fields are not set, an exception is raised
        with self.assertRaises(UserError) as ue:
            self.run_wizard(invoice.id)
        exc_message = ue.exception.args[0]
        self.assertIn("Fiscal Payment Method must be set", exc_message)
        # When fields are set, we can export the e-invoice
        with Form(invoice) as invoice_form:
            invoice_form.fatturapa_payment_method_id = self.env.ref(
                "l10n_it_fiscal_payment_term.fatturapa_mp05"
            )
            invoice_form.fatturapa_payment_term_id = self.env.ref(
                "l10n_it_fiscal_payment_term.fatturapa_tp02"
            )
        res = self.run_wizard(invoice.id)

        # Assert
        attachment = self.attach_model.browse(res["res_id"])
        file_name = "IT06363391001_00019.xml"
        self.set_e_invoice_file_id(attachment, file_name)
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, file_name)

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
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.currency_id = usd
        invoice_form.partner_id = self.res_partner_fatturapa_0
        invoice_form.invoice_date = fields.Date.from_string("2021-12-16")
        invoice_form.invoice_payment_term_id = self.account_payment_term

        self.tax_00_ns.kind_id = self.env.ref("l10n_it_account_tax_kind.n3_2")

        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_00_ns)
        invoice = invoice_form.save()
        invoice.date = fields.Date.from_string("2021-12-16")
        invoice.name = "INV/2021/12/0001"
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
        self.set_e_invoice_file_id(attachment, "IT06363391001_00015a.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00015a.xml")

    def test_16_xml_export(self):
        """
        B2C Customer ITA w fiscalcode w/o vat
        """

        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.res_partner_fatturapa_6
        invoice_form.invoice_date = fields.Date.from_string("2021-12-16")
        invoice_form.invoice_payment_term_id = self.account_payment_term

        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
        invoice = invoice_form.save()
        invoice.date = fields.Date.from_string("2021-12-16")
        invoice.name = "INV/2021/12/0001"
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00016.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00016.xml")

    def test_17_line_related_documents(self):
        # this test is similar to test_2_xml_export, but the related document
        # refers to a line, not the whole invoice
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
                            "sequence": 10,
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
                            "sequence": 20,
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
                        },
                    ),
                ],
            }
        )
        invoice._post()
        # by default, lineRef is assigned from sequence, potentially a wrong guess
        self.assertEqual(invoice.line_ids[1].related_documents[0].lineRef, 20)

        res = self.run_wizard(invoice.id)

        # lineRef is assigned by the template to its actual output value in the XML
        self.assertEqual(invoice.line_ids[1].related_documents[0].lineRef, 2)

        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00017.xml")

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00017.xml")

    def test_no_tax_fail(self):
        """
        - create an invoice with a product line without taxes

        expect to fail with a proper message
        """
        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        invoice_form.partner_id = self.res_partner_fatturapa_0
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.account_id = self.a_sale
            line_form.tax_ids.clear()
        with invoice_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = invoice_form.save()
        invoice.action_post()

        wizard = self.wizard_model.create({})
        with self.assertRaises(UserError) as ue:
            wizard.with_context(active_ids=[invoice.id]).exportFatturaPA()
        error_message = f"Invoice {invoice.name} contains product lines w/o taxes"
        self.assertEqual(ue.exception.args[0], error_message)

    def test_partner_no_address_fail(self):
        """
        - create an XML invoice where the customer has no address or city

        expect to fail with a proper message
        """
        invoice = self._create_invoice()
        invoice.partner_id.street = False
        invoice.partner_id.city = False
        invoice._post()
        wizard = self.wizard_model.create({})
        with self.assertRaises(UserError) as ue:
            wizard.with_context(**{"active_ids": [invoice.id]}).exportFatturaPA()
        error_msg = ue.exception.args[0]
        error_fragments = (
            f"Error processing invoice(s) {invoice.name}",
            "Indirizzo",
            "Comune",
            "Activate debug mode to see the full error",
        )
        for fragment in error_fragments:
            self.assertIn(fragment, error_msg)

        try:
            # Enter debug mode and add details
            mock_request = Mock(
                db=self.env.cr.dbname,
                env=self.env,
                website=False,  # compatibility with website module
                is_frontend=False,
            )
            mock_request.session.debug = "assets"
            odoo.http._request_stack.push(mock_request)
            wizard = self.wizard_model.create({})
            with self.assertRaises(UserError) as ue:
                wizard.with_context(**{"active_ids": [invoice.id]}).exportFatturaPA()
            debug_error_msg = ue.exception.args[0]
            debug_error_fragments = (
                "Full error follows",
                "Reason: value doesn't match any pattern of",
                "p{IsBasicLatin}",
                "<Comune xmlns:ns1",
            )
            for fragment in error_fragments[:-1] + debug_error_fragments:
                self.assertIn(fragment, debug_error_msg)
        finally:
            # Remove from the stack to not interfere with other tests
            odoo.http._request_stack.pop()

    def test_multicompany_fail(self):
        """
        - create two invoices in two different companies
        - try and export both invoices in one single XML file

        expect to fail with a proper message
        """

        self.env.company = self.company
        invoice1 = self._create_invoice()
        invoice1.action_post()

        self.create_2nd_company()
        self.env.company = self.company2
        product2 = self.product_product_10.with_company(company=self.company2.id).copy()
        invoice2 = (
            self.env["account.move"]
            .with_context(
                default_company=self.company2, default_move_type="out_invoice"
            )
            .create(
                {
                    "company_id": self.company2.id,
                    "partner_id": invoice1.partner_id.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product2.id,
                                "tax_ids": [(6, 0, {self.tax_22_c2.id})],
                            },
                        ),
                    ],
                }
            )
        )
        invoice2.action_post()

        self.env.company = self.company
        self.assertEqual(invoice1.company_id, self.company)
        self.assertEqual(invoice2.company_id, self.company2)
        wizard = self.wizard_model.create({})
        with self.assertRaises(UserError) as ue:
            wizard.with_context(active_ids=[invoice1.id, invoice2.id]).exportFatturaPA()
        error_message = "Invoices {}, {} must belong to the same company.".format(
            invoice1.name, invoice2.name
        )
        self.assertEqual(ue.exception.args[0], error_message)

    def test_access_other_user_e_invoice(self):
        """A user can see the e-invoice files created by other users."""
        # Arrange
        user = self.env.user
        other_user = user.copy()
        # pre-condition
        self.assertNotEqual(user, other_user)

        # Act
        with self.with_user(other_user.login):
            e_invoice = self._create_e_invoice()

        # Assert
        self.assertTrue(e_invoice.ir_attachment_id.with_user(user).read())

    def test_unlink(self):
        e_invoice = self._create_e_invoice()
        e_invoice.unlink()
        self.assertFalse(e_invoice.exists())

    def test_reset_to_ready(self):
        e_invoice = self._create_e_invoice()
        e_invoice.state = "sender_error"
        e_invoice.reset_to_ready()
        self.assertEqual(e_invoice.state, "ready")

    def test_preview(self):
        e_invoice = self._create_e_invoice()
        preview_action = e_invoice.ftpa_preview()
        self.assertEqual(preview_action["url"], e_invoice.ftpa_preview_link)

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

    def test_validate_invoice(self):
        """
        Check that the invoice used for tests
        is posted when validated.
        """
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, "draft")

        invoice.action_post()

        self.assertEqual(invoice.state, "posted")

    def test_18_xml_export(self):
        vals = {
            "name": "Azienda Sanmarinese",
            "is_company": "1",
            "street": "Piazza della Libertà",
            "is_pa": False,
            "city": "Città di San Marino",
            "zip": "47890",
            "country_id": self.env.ref("base.sm").id,
            "email": "asm@example.com",
            "vat": "SM00123",
            "codice_destinatario": "2R4GTO8",
        }
        partner_sm = self.env["res.partner"].create(vals)

        tax_kind = self.env["account.tax.kind"].search([("code", "=", "N3.3")], limit=1)
        self.assertTrue(tax_kind)

        vals = {
            "name": "0% SM",
            "amount": 0.0,
            "amount_type": "percent",
            "description": "Non Imponibile Art. 71",
            "kind_id": tax_kind.id,
        }
        tax_id = self.env["account.tax"].create(vals)

        self.env.company.fatturapa_pub_administration_ref = "F000000111"
        invoice = self.invoice_model.create(
            {
                "name": "INV/2016/0013",
                "company_id": self.env.company.id,
                "invoice_date": "2016-01-07",
                "partner_id": partner_sm.id,
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
                            "tax_ids": [(6, 0, [tax_id.id])],
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
                            "tax_ids": [(6, 0, [tax_id.id])],
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
        self.set_e_invoice_file_id(attachment, "IT06363391001_00018.xml")
        self.assertTrue(self.attach_model.file_name_exists("00018"))

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00018.xml")

    def _get_multiple_invoices(self, partner, invoices_number=2):
        """Create `invoices_number` invoices for `partner`."""
        invoices = self.invoice_model.browse()
        for _ in range(invoices_number):
            invoices |= self.init_invoice(
                "out_invoice",
                partner=partner,
                amounts=[
                    100,
                ],
            )
        invoices.action_post()
        return invoices

    def test_max_invoice_number_unlimited(self):
        """Check that when both partner and company do not have any max value,
        only one attachment is created."""

        # pre-condition: partner and company do not have any max value
        company = self.company
        self.assertEqual(company.max_invoice_in_xml, 0)
        partner = self.res_partner_fatturapa_0
        self.assertEqual(partner.max_invoice_in_xml, 0)

        # Create two invoices
        invoices = self._get_multiple_invoices(partner)
        self.run_wizard(invoices.ids)

        # Check that only one attachment is created
        attachments_nbr = len(invoices.mapped("fatturapa_attachment_out_id"))
        self.assertEqual(attachments_nbr, 1)

    def test_max_invoice_number_partner(self):
        """Check that when partner has a max value, company value is ignored and
        many attachments are created."""

        # pre-condition: partner has a value
        company = self.company
        self.assertEqual(company.max_invoice_in_xml, 0)
        partner = self.res_partner_fatturapa_0
        partner.max_invoice_in_xml = 1

        # Create two invoices
        invoices = self._get_multiple_invoices(partner)
        self.run_wizard(invoices.ids)

        # Check that two attachments are created
        attachments_nbr = len(invoices.mapped("fatturapa_attachment_out_id"))
        self.assertEqual(attachments_nbr, 2)

    def test_max_invoice_number_company(self):
        """Check that when company has a max value and partner does not,
        many attachments are created."""

        # pre-condition: only company has a value
        company = self.company
        company.max_invoice_in_xml = 1
        partner = self.res_partner_fatturapa_0
        self.assertEqual(partner.max_invoice_in_xml, 0)

        # Create two invoices
        invoices = self._get_multiple_invoices(partner)
        self.run_wizard(invoices.ids)

        # Check that two attachments are created
        attachments_nbr = len(invoices.mapped("fatturapa_attachment_out_id"))
        self.assertEqual(attachments_nbr, 2)

    def test_hide_descriptive_lines(self):
        """Check that descriptive lines are hidden in the e-invoice
        according to invoice/partner/company configuration."""
        # Arrange
        company = self.company
        partner = self.res_partner_fatturapa_0
        invoice = self.init_invoice(
            "out_invoice",
            partner=partner,
            amounts=[
                100,
            ],
        )
        note_name = "Test note"
        section_name = "Test section"
        with Form(invoice) as invoice_form:
            with invoice_form.invoice_line_ids.new() as section_line:
                section_line.name = section_name
                section_line.display_type = "line_section"
            with invoice_form.invoice_line_ids.new() as note_line:
                note_line.name = note_name
                note_line.display_type = "line_note"
        # Map settings for
        # invoice, partner, company
        # to their expected result
        hide_keys_dict = {
            (False, False, False): "nothing hidden",
            ("none", False, False): "nothing hidden",
            ("note", False, False): "notes hidden",
            ("section", False, False): "sections hidden",
            ("note_section", False, False): "both hidden",
            (False, "note", False): "notes hidden",
            (False, False, "note"): "notes hidden",
            ("none", False, "note"): "nothing hidden",
        }

        for hide_keys, expected_result in hide_keys_dict.items():
            (
                invoice.e_invoice_hide_line_type,
                invoice.partner_id.e_invoice_hide_line_type,
                company.e_invoice_hide_line_type,
            ) = hide_keys
            invoice.action_post()

            # Act
            self.run_wizard(invoice.ids)

            # Assert
            e_invoice = invoice.fatturapa_attachment_out_id
            e_invoice_content = base64.decodebytes(e_invoice.datas).decode()
            if expected_result == "nothing hidden":
                self.assertIn(note_name, e_invoice_content)
                self.assertIn(section_name, e_invoice_content)
            elif expected_result == "notes hidden":
                self.assertNotIn(note_name, e_invoice_content)
                self.assertIn(section_name, e_invoice_content)
            elif expected_result == "sections hidden":
                self.assertIn(note_name, e_invoice_content)
                self.assertNotIn(section_name, e_invoice_content)
            elif expected_result == "both hidden":
                self.assertNotIn(note_name, e_invoice_content)
                self.assertNotIn(section_name, e_invoice_content)
            else:
                self.fail(f"Expected result {expected_result} not managed")

            # cleanup for next loop,
            # without spamming the logs with deleted mail.followers etc.
            with mute_logger("odoo.models.unlink"):
                e_invoice.unlink()
                invoice.button_draft()

    def test_access_wizard_fatturapa_export(self):
        """
        Verify that allowed_report_ids in "wizard.export.fatturapa"
        only contains reports for invoices
        (otherwise non-admin users may not be able to access)
        """
        invoice = self._create_invoice()
        f = Form(
            self.wizard_model.with_context(
                active_id=invoice.id,
                active_model=invoice._name,
            )
        )
        field = f._view["tree"].xpath("//field[@name='report_print_menu']")[0]
        self.assertIn("allowed_report_ids", field.get("domain"))
        allowed_reports = f.allowed_report_ids._get_ids()
        invoice_reports = self.env["ir.actions.report"].search(
            [("binding_model_id", "=", invoice._name)]
        )
        self.assertItemsEqual(invoice_reports.ids, allowed_reports)

        # Verify non-admin user can read the allowed reports
        user = self.user_demo
        self.assertNotIn(self.env.ref("base.group_system"), user.groups_id)
        invoice_reports.with_user(user).read()
