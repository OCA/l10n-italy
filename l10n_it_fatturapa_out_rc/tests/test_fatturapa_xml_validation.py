# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon
from odoo.addons.l10n_it_reverse_charge.tests.rc_common import ReverseChargeCommon


@tagged("post_install", "-at_install")
class TestFatturaPAXMLValidation(ReverseChargeCommon, FatturaPACommon):
    def setUp(self):
        super().setUp()

        # XXX - a company named "YourCompany" already exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )

        self.env.company.name = "YourCompany"
        self.env.company.vat = "IT10538570960"
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

        self.env["decimal.precision"].search(
            [("name", "=", "Product Unit of Measure")]
        ).digits = 3
        self.env["uom.uom"].search([("name", "=", "Units")]).name = "Unit(s)"

        self.rc_type_ieu.partner_type = "other"
        self.rc_type_ieu.partner_id = self.env.company.partner_id.id
        self.rc_type_ieu.fiscal_document_type_id = self.env.ref(
            "l10n_it_fiscal_document_type.15"
        ).id
        self.rc_type_eeu.partner_id = self.env.company.partner_id.id
        self.rc_type_eeu.fiscal_document_type_id = self.env.ref(
            "l10n_it_fiscal_document_type.15"
        ).id
        # l'auto fattura non deve avere la natura di esenzione
        # self.tax_22vi.kind_id = self.env.ref("l10n_it_account_tax_kind.n6").id
        self.supplier_intraEU.customer_rank = 0
        self.bill_sequence_name = "Vendor Bills : Check Number Sequence"
        self.selfinvoice_sequence_name = "selfinvoice : Check Number Sequence"

    @classmethod
    def _create_invoice(cls, move_type, partner, name, invoice_date, ref, taxes):
        invoice_form = Form(
            cls.env["account.move"].with_context({"default_move_type": move_type})
        )
        invoice_form.partner_id = partner
        invoice_form.name = name
        invoice_form.invoice_date = fields.Date.from_string(invoice_date)
        invoice_form.date = fields.Date.from_string(invoice_date)
        invoice_form.ref = ref
        with invoice_form.line_ids.new() as line_form:
            line_form.product_id = cls.env.ref("product.product_product_4d")
            line_form.name = "Invoice for sample product"
            line_form.price_unit = 100
            line_form.tax_ids.clear()
            line_form.tax_ids.add(taxes)
        return invoice_form

    def test_intra_EU(self):
        self.set_sequences(
            15, "2020-12-01", sequence_name=self.selfinvoice_sequence_name
        )
        self.set_sequences(25, "2020-12-01", sequence_name=self.bill_sequence_name)
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id

        invoice_form = self._create_invoice(
            move_type="in_invoice",
            partner=self.supplier_intraEU,
            name="BILL/2021/12/0001",
            invoice_date="2020-12-01",
            ref="EU-SUPPLIER-REF",
            taxes=self.tax_22ai,
        )
        invoice = invoice_form.save()
        invoice.action_post()

        self.assertEqual(
            invoice.rc_self_invoice_id.fiscal_document_type_id.code, "TD17"
        )
        with self.assertRaises(UserError):
            # Impossible to set IdFiscaleIVA
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.vat = "BE0477472701"
        with self.assertRaises(UserError):
            # Street is not set
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.street = "Street"
        self.supplier_intraEU.zip = "12345"
        self.supplier_intraEU.city = "city"
        self.supplier_intraEU.country_id = self.env.ref("base.be")
        self.supplier_intraEU.is_company = True
        res = self.run_wizard(invoice.rc_self_invoice_id.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT10538570960_00002.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, "IT10538570960_00002.xml", "l10n_it_fatturapa_out_rc"
        )

    def test_intra_EU_customer(self):
        self.set_sequences(
            15, "2020-12-01", sequence_name=self.selfinvoice_sequence_name
        )
        self.set_sequences(25, "2020-12-01", sequence_name=self.bill_sequence_name)
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id

        invoice_form = self._create_invoice(
            move_type="out_invoice",
            partner=self.supplier_intraEU,
            name="BILL/2021/12/0002",
            invoice_date="2020-12-01",
            ref="EU-CUSTOMER-REF",
            taxes=self.tax_22vi,
        )
        invoice = invoice_form.save()
        invoice.action_post()
        self.assertFalse(invoice.rc_self_invoice_id)

    def test_intra_EU_draft(self):
        self.set_sequences(
            15, "2020-12-01", sequence_name=self.selfinvoice_sequence_name
        )
        self.set_sequences(25, "2020-12-01", sequence_name=self.bill_sequence_name)
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id

        invoice_form = self._create_invoice(
            move_type="in_invoice",
            partner=self.supplier_intraEU,
            name="BILL/2021/12/0003",
            invoice_date="2020-12-01",
            ref="EU-SUPPLIER-REF",
            taxes=self.tax_22ai,
        )
        invoice = invoice_form.save()
        invoice.action_post()
        invoice.button_cancel()
        self.assertEqual(invoice.state, "cancel")
        self.assertEqual(invoice.state, "cancel")
        self.assertFalse(invoice.rc_self_invoice_id.state)
        invoice.button_draft()
        self.assertEqual(invoice.state, "draft")

    def test_intra_EU_supplier_refund(self):
        self.set_sequences(
            16, "2020-12-01", sequence_name=self.selfinvoice_sequence_name
        )
        self.set_sequences(26, "2020-12-01", sequence_name=self.bill_sequence_name)
        self.supplier_intraEU.property_payment_term_id = self.term_15_30.id

        invoice_form = self._create_invoice(
            move_type="in_refund",
            partner=self.supplier_intraEU,
            name="BILL/2021/12/0004",
            invoice_date="2020-12-01",
            ref="EU-SUPPLIER-REF",
            taxes=self.tax_22ai,
        )
        invoice = invoice_form.save()
        invoice.action_post()
        self.assertEqual(
            invoice.rc_self_invoice_id.fiscal_document_type_id.code, "TD17"
        )
        with self.assertRaises(UserError):
            # Impossible to set IdFiscaleIVA
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.vat = "BE0477472701"
        with self.assertRaises(UserError):
            # Street is not set
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_intraEU.street = "Street"
        self.supplier_intraEU.zip = "12345"
        self.supplier_intraEU.city = "city"
        self.supplier_intraEU.country_id = self.env.ref("base.be")
        self.supplier_intraEU.is_company = True
        res = self.run_wizard(invoice.rc_self_invoice_id.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT10538570960_00003.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, "IT10538570960_00003.xml", "l10n_it_fatturapa_out_rc"
        )

    def test_extra_EU(self):
        self.set_sequences(27, "2020-12-01", sequence_name=self.bill_sequence_name)
        self.supplier_extraEU.property_payment_term_id = self.term_15_30.id
        self.rc_type_eeu.with_supplier_self_invoice = False

        invoice_form = self._create_invoice(
            move_type="in_invoice",
            partner=self.supplier_extraEU,
            name="BILL/2021/12/0005",
            invoice_date="2020-12-01",
            ref="EXEU-SUPPLIER-REF",
            taxes=self.tax_22ae,
        )
        invoice = invoice_form.save()
        invoice.action_post()

        self.assertEqual(
            invoice.rc_self_invoice_id.fiscal_document_type_id.code, "TD17"
        )
        with self.assertRaises(UserError):
            # Impossible to set IdFiscaleIVA
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_extraEU.vat = "US484762844"
        with self.assertRaises(UserError):
            # Street is not set
            self.run_wizard(invoice.rc_self_invoice_id.id)
        self.supplier_extraEU.street = "Street"
        self.supplier_extraEU.zip = "12345"
        self.supplier_extraEU.city = "city"
        self.supplier_extraEU.country_id = self.env.ref("base.us")
        self.supplier_extraEU.is_company = True
        res = self.run_wizard(invoice.rc_self_invoice_id.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT10538570960_00004.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, "IT10538570960_00004.xml", "l10n_it_fatturapa_out_rc"
        )
