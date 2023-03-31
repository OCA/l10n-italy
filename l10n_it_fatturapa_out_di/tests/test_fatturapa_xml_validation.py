# Copyright 2021 Marco Colombo https://github.com/TheMule71

import base64

from odoo import fields
from odoo.tests import Form, tagged

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

        self.env.ref("product.decimal_product_uom").digits = 3
        self.env.ref("uom.product_uom_unit").name = "Unit(s)"

        tax_form = Form(self.env["account.tax"])
        tax_form.name = "22%"
        tax_form.amount = 22
        self.tax22 = tax_form.save()

        tax_form = Form(self.env["account.tax"])
        tax_form.name = "FC INC"
        tax_form.amount = 0
        tax_form.price_include = True
        tax_form.kind_id = self.env.ref("l10n_it_account_tax_kind.n3_5")
        tax_form.law_reference = "Art. 8 co. 1 lett. c) e co. 2 del DPR 633/72"
        self.tax1 = tax_form.save()

        fp_form = Form(self.env["account.fiscal.position"])
        fp_form.name = "Test for declaration"
        fp_form.valid_for_declaration_of_intent = True
        with fp_form.tax_ids.new() as tax_ids:
            tax_ids.tax_src_id = self.tax22
            tax_ids.tax_dest_id = self.tax1
        self.fiscal_position = fp_form.save()

        self.payment_term = self.env.ref(
            "account.account_payment_term_end_following_month"
        )
        with Form(self.payment_term) as pt_form:
            pt_form.fatturapa_pt_id = self.env.ref(
                "l10n_it_fiscal_payment_term.fatturapa_tp02"
            )
            pt_form.fatturapa_pm_id = self.env.ref(
                "l10n_it_fiscal_payment_term.fatturapa_mp05"
            )

        self.env.ref("l10n_it_declaration_of_intent.declaration_of_intent_seq").copy(
            {
                "company_id": self.env.company.id,
            }
        )

    def _create_declaration(self):
        dec_form = Form(self.env["l10n_it_declaration_of_intent.declaration"])
        dec_form.partner_id = self.res_partner_fatturapa_0
        dec_form.date = fields.Date.from_string("2016-06-15")
        dec_form.date_start = fields.Date.from_string("2016-06-15")
        dec_form.date_end = fields.Date.today()
        dec_form.taxes_ids.add(self.tax1)
        dec_form.limit_amount = 1000.00
        dec_form.fiscal_position_id = self.fiscal_position
        dec_form.type = "out"
        dec_form.telematic_protocol = "08060120341234567-000001"
        dec_form.partner_document_number = "DI/111"
        dec_form.partner_document_date = fields.Date.from_string("2016-06-15")
        dec = dec_form.save()
        return dec

    def _create_invoice(self):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.date = fields.Date.from_string("2016-06-15")
        move_form.invoice_date = fields.Date.from_string("2016-06-15")
        move_form.invoice_date_due = fields.Date.today()
        move_form.partner_id = self.res_partner_fatturapa_0
        move_form.invoice_payment_term_id = self.payment_term
        move_form.fiscal_position_id = self.fiscal_position

        with move_form.line_ids.new() as line_form:
            line_form.product_id = self.product_product_10
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax1)
        invoice = move_form.save()
        return invoice

    def test_1_di_xml_export(self):
        dec = self._create_declaration()
        invoice = self._create_invoice()
        invoice.declaration_of_intent_ids = [(6, 0, [dec.id])]
        invoice.invoice_line_ids.filtered("product_id")[
            0
        ].force_declaration_of_intent_id = dec
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")

    def test_2_di_xml_export(self):
        dec = self._create_declaration()
        invoice = self._create_invoice()
        invoice.declaration_of_intent_ids = [(6, 0, [dec.id])]
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00002.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00002.xml")

    def test_3_di_xml_export(self):
        dec2 = self._create_declaration()
        dec2.telematic_protocol = "08060120341234567-000002"
        dec2.partner_document_number = "DI/112"

        dec1 = self._create_declaration()

        invoice = self._create_invoice()
        invoice.declaration_of_intent_ids = [
            (
                6,
                0,
                [
                    dec1.id,
                    dec2.id,
                ],
            )
        ]
        invoice.invoice_line_ids.filtered("product_id")[
            0
        ].force_declaration_of_intent_id = dec2
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00003.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00003.xml")
