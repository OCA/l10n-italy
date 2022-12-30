# Copyright 2021 Marco Colombo - Phi srl

import base64

from lxml import etree

from odoo import fields
from odoo.tests import Form, tagged

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestFatturaOutNoteLine(FatturaPACommon):
    def setUp(self):
        super().setUp()
        self.env.company.vat = "IT06363391001"
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

    def test_1_note_taxes(self):
        """test case:
        - company default 22%
        - one product 10%
        - one note

        expected result: one DatiRiepilogo with AliquotaIVA == 10%
        """
        self.env.company.account_sale_tax_id = self.tax_22

        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.name = "INV/2016/0013"
        move_form.invoice_date = fields.Date.from_string("2016-01-07")
        move_form.partner_id = self.res_partner_fatturapa_0
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_10)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = move_form.save()

        res = self.run_wizard(invoice.id)
        self.assertTrue(res)

        attachment = self.attach_model.browse(res["res_id"])
        xml_content = base64.decodebytes(attachment.datas)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        aliquote = xml.findall(".//DatiRiepilogo/AliquotaIVA")
        self.assertEqual(len(aliquote), 1)
        self.assertEqual(aliquote[0].text, "10.00")

    def test_2_note_taxes(self):
        """test case:
        - company default 22%
        - one product 22%
        - one note

        expected result: one DatiRiepilogo with AliquotaIVA == 22%
        """
        self.env.company.account_sale_tax_id = self.tax_22

        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.name = "INV/2016/0013"
        move_form.invoice_date = fields.Date.from_string("2016-01-07")
        move_form.partner_id = self.res_partner_fatturapa_0
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_22)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = move_form.save()

        res = self.run_wizard(invoice.id)
        self.assertTrue(res)

        attachment = self.attach_model.browse(res["res_id"])
        xml_content = base64.decodebytes(attachment.datas)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        aliquote = xml.findall(".//DatiRiepilogo/AliquotaIVA")
        self.assertEqual(len(aliquote), 1)
        self.assertEqual(aliquote[0].text, "22.00")

    def test_3_note_taxes(self):
        """test case:
        - company default 22%
        - one product 22%
        - one product 10%
        - one note

        expected result:
        - one DatiRiepilogo with AliquotaIVA == 10%
        - one DatiRiepilogo with AliquotaIVA == 22%
        (order irrelevant)
        """
        self.env.company.account_sale_tax_id = self.tax_22

        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.name = "INV/2016/0013"
        move_form.invoice_date = fields.Date.from_string("2016-01-07")
        move_form.partner_id = self.res_partner_fatturapa_0
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_22)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_10)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = move_form.save()

        res = self.run_wizard(invoice.id)
        self.assertTrue(res)

        attachment = self.attach_model.browse(res["res_id"])
        xml_content = base64.decodebytes(attachment.datas)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        aliquote = xml.findall(".//DatiRiepilogo/AliquotaIVA")
        self.assertEqual(len(aliquote), 2)
        if aliquote[0].text == "22.00":
            self.assertEqual(aliquote[1].text, "10.00")
        else:
            self.assertEqual(aliquote[0].text, "10.00")
            self.assertEqual(aliquote[1].text, "22.00")

    def test_4_note_taxes(self):
        """test case:
        - company default 22%
        - one product 22%, price 10
        - one note
        save & edit
        - product price to 0
        save & export

        expected result:
        - one DatiRiepilogo with AliquotaIVA == 22%
        """
        self.env.company.account_sale_tax_id = self.tax_22

        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.name = "INV/2016/0013"
        move_form.invoice_date = fields.Date.from_string("2016-01-07")
        move_form.partner_id = self.res_partner_fatturapa_0
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.price_unit = 10.0
            line_form.quantity = 1
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_22)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = move_form.save()

        with Form(invoice) as move_form:
            with move_form.invoice_line_ids.edit(0) as line_form:
                line_form.price_unit = 0.0

        res = self.run_wizard(invoice.id)
        self.assertTrue(res)

        attachment = self.attach_model.browse(res["res_id"])
        xml_content = base64.decodebytes(attachment.datas)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        aliquote = xml.findall(".//DatiRiepilogo/AliquotaIVA")
        self.assertEqual(len(aliquote), 1)
        self.assertEqual(aliquote[0].text, "22.00")

    def test_5_note_tax_kind_id(self):
        """test case:
        - company default 22%
        - one product 0%, tax having kind_id
        - one note

        expected result: one DatiRiepilogo with AliquotaIVA == 0%
        """
        self.env.company.account_sale_tax_id = self.tax_22

        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.name = "INV/2016/0013"
        move_form.invoice_date = fields.Date.from_string("2016-01-07")
        move_form.partner_id = self.res_partner_fatturapa_0
        with move_form.invoice_line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.remove(index=0)
            line_form.tax_ids.add(self.tax_00_ns)
        with move_form.invoice_line_ids.new() as line_form:
            line_form.display_type = "line_note"
            line_form.name = "just a note"
            line_form.account_id = self.env["account.account"]
        invoice = move_form.save()

        res = self.run_wizard(invoice.id)
        self.assertTrue(res)

        attachment = self.attach_model.browse(res["res_id"])
        xml_content = base64.decodebytes(attachment.datas)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        aliquote = xml.findall(".//DatiRiepilogo/AliquotaIVA")
        self.assertEqual(len(aliquote), 1)
        self.assertEqual(aliquote[0].text, "0.00")
