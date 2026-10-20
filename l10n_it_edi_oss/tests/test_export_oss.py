#  Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import Form

from .common import Common


class TestExportOss(Common):
    def setUp(self):
        super().setUp()

        tax_au_oss_form = Form(self.env["account.tax"].with_company(self.company))
        tax_au_oss_form.name = "OSS AU"
        tax_au_oss_form.amount = 20.0
        tax_au_oss_form.l10n_it_exempt_reason = "N3.2"
        tax_au_oss_form.l10n_it_law_reference = (
            "NON IMPONIBILE ART. 41 COMMA 1, LETT. B"
        )
        self.tax_au_oss = tax_au_oss_form.save()
        self.tax_au_oss.oss_country_id = self.env.ref("base.at").id

        fp_form = Form(self.env["account.fiscal.position"].with_company(self.company))
        fp_form.name = "OSS Test"
        with fp_form.tax_ids.new() as tax_form:
            tax_form.tax_src_id = self.default_tax
            tax_form.tax_dest_id = self.tax_au_oss
        self.fiscal_position_oss = fp_form.save()

        self.eu_b2c_customer = self.env["res.partner"].create(
            {
                "name": "EU B2C Customer",
                "customer_rank": 1,
                "is_company": False,
                "street": "11 Wien St",
                "city": "Wolfsgraben",
                "zip": "12345",
                "country_id": self.env.ref("base.at").id,
                "l10n_it_pa_index": "XXXXXXX",
                "invoice_edi_format": "it_edi_xml",
            }
        )

    def _create_invoice(self, date):
        move_form = Form(
            self.env["account.move"]
            .with_company(self.company)
            .with_context(default_move_type="out_invoice")
        )
        move_form.invoice_date = fields.Date.from_string(date)
        move_form.invoice_date_due = move_form.invoice_date
        move_form.partner_id = self.eu_b2c_customer
        with move_form.invoice_line_ids.new() as line_form:
            line_form.name = "test line"
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.default_tax)
        account_move = move_form.save()
        return account_move

    def test_1_oss_xml_export(self):
        date = "2022-02-28"
        invoice = self._create_invoice(date)
        move_form = Form(invoice)
        move_form.fiscal_position_id = self.fiscal_position_oss
        with move_form.invoice_line_ids.edit(0) as line_form:
            line_form.tax_ids.clear()
            line_form.tax_ids.add(self.tax_au_oss)
        invoice = move_form.save()
        self.assertEqual(
            fields.first(invoice.invoice_line_ids).tax_ids[:1].name,
            self.tax_au_oss.name,
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "IT01234560157_00001.xml")

    def test_2_oss_xml_export(self):
        date = "2023-02-28"
        invoice = self._create_invoice(date)
        self.assertEqual(
            fields.first(invoice.invoice_line_ids).tax_ids[:1].name,
            self.default_tax.name,
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "IT01234560157_00002.xml")
