#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from psycopg2 import IntegrityError

from odoo.exceptions import UserError, ValidationError
from odoo.modules import get_module_resource
from odoo.tests import Form
from odoo.tools import mute_logger

from .fatturapa_common import FatturapaCommon


class TestDuplicatedAttachment(FatturapaCommon):
    def test_duplicated_attachment(self):
        """Attachment name must be unique"""
        # This test breaks the current transaction
        # and every test executed after this in the
        # same transaction would fail.
        # Note that all the tests in TestFatturaPAXMLValidation
        # are executed in the same transaction.
        self.run_wizard("test_duplicated", "IT02780790107_11005.xml")
        with self.assertRaises(IntegrityError) as ie:
            with mute_logger("odoo.sql_db"):
                self.run_wizard("test_duplicated", "IT02780790107_11005.xml")
        self.assertEqual(ie.exception.pgcode, "23505")


class TestFatturaPAXMLValidation(FatturapaCommon):
    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.wt = self.create_wt_4q()
        self.wtq = self.create_wt_27_20q()
        self.wt4q = self.create_wt_26_40q()
        self.wt2q = self.create_wt_26_20q()
        self.invoice_model = self.env["account.move"]
        self.wizard_link_inv_line_model = self.env["wizard.link.to.invoice.line"]

    def test_00_xml_import(self):
        self.env.company.cassa_previdenziale_product_id = self.service.id
        res = self.run_wizard("test0", "IT05979361218_001.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.register_code, "TO1258B")
        self.assertEqual(invoice.partner_id.register_fiscalpos.code, "RF02")
        self.assertEqual(invoice.ref, "FT/2015/0006")
        self.assertEqual(invoice.payment_reference, "FT/2015/0006")
        self.assertEqual(invoice.amount_total, 57.00)
        self.assertEqual(invoice.gross_weight, 0.00)
        self.assertEqual(invoice.net_weight, 0.00)
        self.assertEqual(invoice.welfare_fund_ids[0].kind_id.code, "N4")
        self.assertFalse(invoice.art73)
        welfare_found = False
        for line in invoice.invoice_line_ids:
            if line.product_id.id == self.service.id:
                self.assertAlmostEqual(line.price_unit, 3)
                welfare_found = True
        self.assertTrue(welfare_found)
        self.assertTrue(len(invoice.e_invoice_line_ids) == 1)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].name, "Prodotto di test al giorno"
        )
        self.assertEqual(invoice.e_invoice_line_ids[0].qty, 15)
        self.assertEqual(invoice.e_invoice_line_ids[0].uom, "Giorno(i)")
        self.assertEqual(invoice.e_invoice_line_ids[0].unit_price, 3.6)
        self.assertEqual(invoice.e_invoice_line_ids[0].total_price, 54)
        self.assertEqual(invoice.e_invoice_line_ids[0].tax_amount, 0)
        self.assertEqual(invoice.e_invoice_line_ids[0].tax_kind, "N4")
        self.assertTrue(len(invoice.e_invoice_line_ids[0].other_data_ids) == 2)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].other_data_ids[0].text_ref, "Riferimento"
        )
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14001"

    def test_01_xml_import(self):
        res = self.run_wizard("test1", "IT02780790107_11004.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "123")
        self.assertEqual(invoice.payment_reference, "123")
        self.assertEqual(invoice.amount_untaxed, 34.00)
        self.assertEqual(invoice.amount_tax, 7.48)
        self.assertEqual(len(invoice.invoice_line_ids[0].tax_ids), 1)
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids[0].name, "22% e-bill")
        self.assertEqual(invoice.fatturapa_summary_ids[0].amount_untaxed, 34.00)
        self.assertEqual(invoice.fatturapa_summary_ids[0].amount_tax, 7.48)
        self.assertEqual(invoice.fatturapa_summary_ids[0].payability, "D")
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(invoice.partner_id.state_id.code, "SS")
        self.assertEqual(invoice.partner_id.country_id.code, "IT")
        self.assertEqual(invoice.partner_id.vat, "IT02780790107")
        self.assertEqual(invoice.tax_representative_id.name, "Rappresentante fiscale")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_rate_tax, 0.04)
        order_related_doc = invoice.related_documents.filtered(
            lambda rd: rd.type == "order"
        )
        self.assertTrue(order_related_doc)
        self.assertEqual(order_related_doc.cig, "456def")
        self.assertEqual(order_related_doc.cup, "123abc")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_amount_tax, 9)
        self.assertFalse(invoice.welfare_fund_ids[0].welfare_taxable)
        self.assertEqual(invoice.unit_weight, "KGM")
        self.assertEqual(invoice.ftpa_incoterms, "DAP")
        self.assertEqual(invoice.fiscal_document_type_id.code, "TD01")
        self.assertTrue(invoice.art73)

        # verify if attached documents are correctly imported
        attachments = invoice.fatturapa_doc_attachments
        self.assertEqual(len(attachments), 1)
        orig_attachment_path = get_module_resource(
            "l10n_it_fatturapa_in", "tests", "data", "test.png"
        )
        with open(orig_attachment_path, "rb") as orig_attachment:
            orig_attachment_data = orig_attachment.read()
            self.assertEqual(attachments[0].raw, orig_attachment_data)

        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14011"

    def test_02_xml_import(self):
        res = self.run_wizard("test02", "IT05979361218_011.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.intermediary.vat, "IT03339130126")

    def test_04_xml_import(self):
        res = self.run_wizard("test4", "IT02780790107_11005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "124")
        self.assertEqual(invoice.payment_reference, "124")
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids[0].name, "22% e-bill")
        self.assertEqual(invoice.invoice_line_ids[1].tax_ids[0].name, "22% e-bill")
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids[0].amount, 22)
        self.assertEqual(invoice.invoice_line_ids[1].tax_ids[0].amount, 22)
        self.assertAlmostEqual(invoice.invoice_line_ids[1].price_unit, 2)
        self.assertTrue(len(invoice.e_invoice_line_ids) == 2)
        for e_line in invoice.e_invoice_line_ids:
            self.assertTrue(e_line.line_number in (1, 2))
            if e_line.line_number == 1:
                self.assertEqual(e_line.cod_article_ids[0].name, "EAN")
                self.assertEqual(e_line.cod_article_ids[0].code_val, "12345")
        self.assertEqual(
            invoice.inconsistencies,
            "Company Name field contains 'Societa' "
            "Alpha SRL'. Your System contains 'SOCIETA' ALPHA SRL'\n\n",
        )
        # allow following test to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14041"

    def test_05_xml_import(self):
        res = self.run_wizard("test5", "IT05979361218_003.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "FT/2015/0008")
        self.assertEqual(invoice.payment_reference, "FT/2015/0008")
        self.assertEqual(invoice.sender, "TZ")
        self.assertEqual(invoice.intermediary.name, "MARIO ROSSI")
        self.assertEqual(invoice.intermediary.firstname, "MARIO")
        self.assertEqual(invoice.intermediary.lastname, "ROSSI")
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].name, "SC"
        )
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].percentage, 10
        )
        self.assertEqual(invoice.amount_untaxed, 9)
        self.assertEqual(invoice.amount_tax, 0)
        self.assertEqual(invoice.amount_total, 9)

    def test_06_import_except(self):
        # File not exist Exception
        self.assertRaises(Exception, self.run_wizard, "test6_Exception", "")

        # fake Signed file is passed , generate parsing error
        with mute_logger("odoo.addons.l10n_it_fatturapa_in.models.attachment"):
            attachment = self.create_attachment(
                "test6_orm_exception", "IT05979361218_fake.xml.p7m"
            )
        self.assertIn("Invalid xml", attachment.e_invoice_parsing_error)

    def test_07_xml_import(self):
        # 2 lines with quantity != 1 and discounts
        res = self.run_wizard("test7", "IT05979361218_004.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "FT/2015/0009")
        self.assertEqual(invoice.payment_reference, "FT/2015/0009")
        self.assertAlmostEqual(invoice.amount_untaxed, 1173.60)
        self.assertEqual(invoice.amount_tax, 258.19)
        self.assertEqual(invoice.amount_total, 1431.79)
        self.assertAlmostEqual(
            invoice.e_invoice_amount_untaxed,
            invoice.amount_untaxed,
            places=invoice.currency_id.decimal_places,
        )
        self.assertAlmostEqual(
            invoice.e_invoice_amount_tax,
            invoice.amount_tax,
            places=invoice.currency_id.decimal_places,
        )
        self.assertEqual(invoice.e_invoice_validation_error, False)
        self.assertEqual(invoice.invoice_line_ids[0].admin_ref, "D122353")

    def test_08_xml_import(self):
        # using ImportoTotaleDocumento
        res = self.run_wizard("test8", "IT05979361218_005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "FT/2015/0010")
        self.assertEqual(invoice.payment_reference, "FT/2015/0010")
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertFalse(invoice.inconsistencies)
        # allow following test to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14081"

    def test_08_xml_import_no_account(self):
        """Check that a useful error message is raised when
        the credit account is missing in journal."""
        company = self.env.company
        journal = self.wizard_model.get_journal(company)
        journal_account = journal.default_account_id
        journal.default_account_id = False

        expense_default_property = self.env["ir.property"]._get_property(
            "property_account_expense_categ_id",
            "product.category",
            res_id=False,
        )
        # Setting res_id disables the property from acting as default value
        expense_default_property.res_id = 1
        with self.assertRaises(UserError) as ue:
            res = self.run_wizard("test8_no_account", "IT05979361218_005.xml")
            # allow following code to reuse the same XML file
            invoice_id = res.get("domain")[0][2][0]
            invoice = self.invoice_model.browse(invoice_id)
            invoice.ref = invoice.payment_reference = "14082"
        self.assertIn(journal.display_name, ue.exception.args[0])
        self.assertIn(company.display_name, ue.exception.args[0])

        discount_amount = -143.18

        # Restore the property and import the invoice
        expense_default_property.res_id = False
        res = self.run_wizard("test8_with_property", "IT05979361218_005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        invoice_lines = invoice.invoice_line_ids
        discount_line = invoice_lines.filtered(
            lambda line: line.price_unit == discount_amount
        )
        self.assertEqual(
            discount_line.account_id,
            expense_default_property.get_by_record(),
        )
        # allow following code to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14083"

        # Restore the property and import the invoice
        journal.default_account_id = journal_account
        res = self.run_wizard("test8_with_journal", "IT05979361218_005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        invoice_lines = invoice.invoice_line_ids
        discount_line = invoice_lines.filtered(
            lambda line: line.price_unit == discount_amount
        )
        self.assertEqual(
            discount_line.account_id,
            journal_account,
        )
        self.assertTrue(invoice)
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14084"

    def test_09_xml_import(self):
        # using DatiGeneraliDocumento.ScontoMaggiorazione without
        # ImportoTotaleDocumento
        # add test file name case sensitive
        res = self.run_wizard("test9", "IT05979361218_006.XML")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "FT/2015/0011")
        self.assertEqual(invoice.payment_reference, "FT/2015/0011")
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertEqual(
            invoice.inconsistencies,
            "Computed amount untaxed 1030.42 is different from" " summary data 1173.6",
        )

    def test_10_xml_import(self):
        # Fix Date format
        res = self.run_wizard("test6", "IT05979361218_007.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "FT/2015/0009")
        self.assertEqual(invoice.payment_reference, "FT/2015/0009")
        self.assertEqual(invoice.invoice_date, date(2015, 3, 16))
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_due_date,
            date(2015, 6, 3),
        )
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].fatturapa_pm_id.code,
            "MP18",
        )

    def test_11_xml_import(self):
        # DatiOrdineAcquisto with RiferimentoNumeroLinea referring to
        # not existing invoice line
        res = self.run_wizard("test11", "IT02780790107_11006.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(len(invoice.invoice_line_ids[0].related_documents), 0)
        self.assertEqual(invoice.invoice_line_ids[0].sequence, 1)
        self.assertEqual(invoice.related_documents[0].type, "order")
        self.assertEqual(invoice.related_documents[0].lineRef, 60)
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14111"

    def test_12_xml_import(self):
        res = self.run_wizard("test12", "IT05979361218_008.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.payment_reference, "FT/2015/0012")
        self.assertEqual(invoice.sender, "TZ")
        self.assertEqual(invoice.intermediary.name, "MARIO ROSSI")
        self.assertEqual(invoice.intermediary.firstname, "MARIO")
        self.assertEqual(invoice.intermediary.lastname, "ROSSI")

    def test_13_xml_import(self):
        # inconsistencies must not be duplicated
        res = self.run_wizard_multi(
            [
                "IT02780790107_11005.xml",
                "IT02780790107_11006.xml",
            ]
        )
        invoice1_id = res.get("domain")[0][2][0]
        invoice2_id = res.get("domain")[0][2][1]
        invoice1 = self.invoice_model.browse(invoice1_id)
        invoice2 = self.invoice_model.browse(invoice2_id)
        self.assertEqual(
            invoice1.inconsistencies,
            "Company Name field contains 'Societa' "
            "Alpha SRL'. Your System contains 'SOCIETA' ALPHA SRL'\n\n",
        )
        self.assertEqual(
            invoice2.inconsistencies,
            "Company Name field contains 'Societa' "
            "Alpha SRL'. Your System contains 'SOCIETA' ALPHA SRL'\n\n",
        )

    def test_14_xml_import(self):
        # check: no tax code found , write inconsisteance and anyway
        # create draft
        res = self.run_wizard("test14", "IT02780790107_11007.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.ref, "136")
        self.assertEqual(invoice.payment_reference, "136")
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.amount_untaxed, 25.00)
        self.assertEqual(invoice.amount_tax, 0.0)
        self.assertEqual(
            invoice.inconsistencies,
            "Company Name field contains 'Societa' "
            "Alpha SRL'. Your System contains 'SOCIETA' ALPHA SRL'\n\n"
            "XML contains tax with percentage '15.55'"
            " but it does not exist in your system",
        )

    def test_15_xml_import(self):
        self.wt = self.create_wt()
        res = self.run_wizard("test15", "IT05979361218_009.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.withholding_tax_amount, 1)
        self.assertAlmostEqual(invoice.amount_total, 6.1)
        self.assertAlmostEqual(invoice.amount_net_pay, 5.1)

    def test_16_xml_import(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        res = self.run_wizard("test16a", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, "")
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.ref in ("456", "123"))
            self.assertTrue(invoice.payment_reference in ("456", "123"))
            if invoice.ref == "123":
                self.assertTrue(len(invoice.invoice_line_ids) == 2)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)
                self.assertEqual(invoice.invoice_date_due, date(2015, 1, 30))
            if invoice.ref == "456":
                self.assertTrue(len(invoice.invoice_line_ids) == 1)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)
                self.assertEqual(invoice.invoice_date_due, date(2015, 1, 28))
        # allow following code to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14161"
        invoices[1].ref = invoices[1].payment_reference = "14162"

        partner = invoice.partner_id
        partner.e_invoice_default_product_id = self.imac.product_variant_ids[0].id
        # I create a supplier code to be matched in XML
        self.env["product.supplierinfo"].create(
            {
                "name": partner.id,
                "product_tmpl_id": self.headphones.id,
                "product_code": "ART123",
            }
        )
        res = self.run_wizard("test16b", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        for invoice in invoices:
            self.assertTrue(invoice.ref in ("456", "123"))
            self.assertTrue(invoice.payment_reference in ("456", "123"))
            if invoice.ref == "123":
                self.assertEqual(
                    invoice.invoice_line_ids[0].product_id.id,
                    self.headphones.product_variant_ids[0].id,
                )
            else:
                for line in invoice.invoice_line_ids:
                    self.assertEqual(
                        line.product_id.id, self.imac.product_variant_ids[0].id
                    )
        # allow following code to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14163"
        invoices[1].ref = invoices[1].payment_reference = "14164"

        # change Livello di dettaglio Fatture elettroniche to Minimo
        partner.e_invoice_detail_level = "0"
        res = self.run_wizard("test16c", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertTrue(len(invoices) == 2)
        for invoice in invoices:
            self.assertTrue(len(invoice.invoice_line_ids) == 0)
            self.assertTrue(invoice.move_type == "in_invoice")
        # allow following tests to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14165"
        invoices[1].ref = invoices[1].payment_reference = "14166"

    def test_03_xml_import(self):
        # Testing CAdES signature
        res = self.run_wizard("test18", "IT01234567890_FPR03.xml.p7m")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, "")
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.ref in ("456", "123"))
            self.assertTrue(invoice.payment_reference in ("456", "123"))
            if invoice.ref == "123":
                self.assertTrue(len(invoice.invoice_line_ids) == 2)
            if invoice.ref == "456":
                self.assertTrue(len(invoice.invoice_line_ids) == 1)
        # allow following tests to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14031"
        invoices[1].ref = invoices[1].payment_reference = "14032"

    def test_17_xml_import(self):
        res = self.run_wizard("test17", "IT05979361218_010.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.related_documents[0].type, "invoice")

    def test_19_xml_import(self):
        # Testing CAdES signature, base64 encoded
        res = self.run_wizard(
            "test19",
            "IT01234567890_FPR03.base64.xml.p7m",
        )
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertEqual(invoice.partner_id.e_invoice_detail_level, "0")
            self.assertTrue(invoice.ref in ("456", "123"))
            self.assertTrue(invoice.payment_reference in ("456", "123"))
            if invoice.ref == "123":
                self.assertEqual(
                    invoice.inconsistencies,
                    "Computed amount untaxed 0.0 is different from summary "
                    "data 25.0",
                )
            if invoice.ref == "456":
                self.assertEqual(
                    invoice.inconsistencies,
                    "Computed amount untaxed 0.0 is different from summary "
                    "data 2000.0",
                )
        # allow following tests to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14191"
        invoices[1].ref = invoices[1].payment_reference = "14192"

    def test_20_xml_import(self):
        # Testing xml without xml declaration (sent by Amazon)
        res = self.run_wizard("test20", "IT05979361218_no_decl.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

    def test_21_xml_import(self):
        supplier = self.env["res.partner"].search([("vat", "=", "IT02780790107")])[0]
        # in order to make the system create the invoice lines
        supplier.e_invoice_detail_level = "2"
        res = self.run_wizard("test21", "IT01234567890_FPR04.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.inconsistencies, "")
        self.assertEqual(invoice.invoice_line_ids[2].price_unit, 0.0)
        self.assertEqual(invoice.invoice_line_ids[2].discount, 0.0)

    def test_22_xml_import(self):
        res = self.run_wizard("test22", "IT02780790107_11004_xml_doctor.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

        self.assertIn("removed timezone information", invoice.inconsistencies)

        # DatiGeneraliDocumento/Causale
        self.assertIn(" ", invoice.narration)

        # DatiGeneraliDocumento/Data
        self.assertEqual(invoice.invoice_date, date(2014, 12, 18))

        # DatiTrasporto/IndirizzoResa/NumeroCivico
        self.assertEqual(
            invoice.delivery_address, "strada dei test,  \n12042 - Bra\nCN IT"
        )

        # DatiTrasporto/DataOraConsegna
        self.assertFalse(invoice.delivery_datetime)

        # DatiBeniServizi/DettaglioLinee/Descrizione

        # test commented because I'n not sure about expected behavior on 14.0
        # actually, name is recalculated based product (see
        # account._move_autocomplete_invoice_lines_values)
        # self.assertEqual(invoice.invoice_line_ids[0].name, " ")

        # DatiPagamento/DettaglioPagamento/DataDecorrenzaPenale
        payment_data = self.env["fatturapa.payment.data"].search(
            [("invoice_id", "=", invoice.id)]
        )
        self.assertEqual(
            payment_data[0].payment_methods[0].penalty_date, date(2015, 5, 1)
        )
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14221"

    def test_23_xml_import(self):
        # Testing CAdES signature, base64 encoded with newlines
        res = self.run_wizard(
            "test23",
            "IT01234567890_FPR04.base64.xml.p7m",
        )
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        # allow following tests to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14231"
        invoices[1].ref = invoices[1].payment_reference = "14232"

    def test_24_xml_import(self):
        res = self.run_wizard("test24", "IT05979361218_012.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(
            invoice.inconsistencies,
            "Computed amount untaxed 34.32 is different from" " summary data 34.67",
        )

    def test_25_xml_import(self):
        res = self.run_wizard("test25", "IT05979361218_013.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.67)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)
        self.assertEqual(invoice.efatt_rounding, -0.35)
        invoice.action_post()
        move_line = False
        for line in invoice.line_ids:
            if (
                line.account_id.id
                == self.env.company.arrotondamenti_attivi_account_id.id
            ):
                move_line = True
        self.assertTrue(move_line)

    def test_26_xml_import(self):
        res = self.run_wizard("test26", "IT05979361218_015.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.32)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)

    def test_30_xml_import(self):
        self.env.company.cassa_previdenziale_product_id = self.service.id
        res = self.run_wizard("test30", "IT05979361218_001.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        partner_id = invoice.partner_id
        partner_id.write(
            {
                "street": "Viale Repubblica, 34",
                "electronic_invoice_no_contact_update": True,
            }
        )
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14301"

        res = self.run_wizard("test30a", "IT05979361218_002.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.id, partner_id.id)
        self.assertEqual(invoice.partner_id.street, "Viale Repubblica, 34")
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14302"

    def test_31_xml_import(self):
        res = self.run_wizard("test31", "IT01234567890_FPR05.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[1].discount, 100)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, 0)
        self.assertEqual(round(invoice.amount_total, 2), 12.2)

    def test_32_xml_import(self):
        # Refund with positive total
        res = self.run_wizard("test32", "IT01234567890_FPR06.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.move_type, "in_refund")
        self.assertEqual(invoice.amount_total, 18.3)
        self.assertAlmostEqual(invoice.invoice_line_ids[0].price_unit, 2.0)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 10.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 20.0)
        self.assertAlmostEqual(invoice.invoice_line_ids[1].price_unit, -1.0)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 5.0)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, -5.0)

    def test_33_xml_import(self):
        # Refund with negative total
        res = self.run_wizard("test33", "IT01234567890_FPR07.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.move_type, "in_refund")
        self.assertEqual(round(invoice.amount_total, 2), 24.4)
        self.assertAlmostEqual(invoice.invoice_line_ids[0].price_unit, 2.0)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 10.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 20.0)
        self.assertEqual(invoice.e_invoice_amount_untaxed, -20.0)
        self.assertEqual(invoice.e_invoice_amount_tax, -4.4)

    def test_34_xml_import(self):
        # No Ritenuta lines set
        res = self.run_wizard("test34", "IT01234567890_FPR08.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains DatiRitenuta but no lines subjected to Ritenuta was "
            "found. Please manually check Withholding tax Amount\nE-bill contains "
            "ImportoRitenuta 360.0 but created invoice has got 0.0\n.",
        )

    def test_35_xml_import(self):
        # creating 2350 before 2320, so odoo will use 2350 but e-invoices
        # contains 2320: error message must appear
        self.create_wt_23_50()
        self.create_wt_23_20()
        res = self.run_wizard("test35", "IT01234567890_FPR09.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains ImportoRitenuta 30.16 but created invoice has got "
            "75.41\n.",
        )

    def test_36_xml_import(self):
        # creating a res.bank and importing an XML without "IstitutoFinanziario"
        self.create_res_bank()
        res = self.run_wizard("test36", "IT01234567890_FPR10.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_bank.bank_id.bic,
            "BCITITMM",
        )
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_bank.bank_id.name,
            "Banca generica",
        )

    def test_37_xml_import_dates(self):
        self.env.user.lang = "it_IT"
        res = self.run_wizard("test37", "IT02780790107_11004.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.fatturapa_attachment_in_id.invoices_date, "18/12/2014")
        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14371"

    def test_38_xml_import_dates(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        self.env.user.lang = "it_IT"
        res = self.run_wizard("test38", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        self.assertEqual(
            invoices[0].fatturapa_attachment_in_id.invoices_date,
            "18/12/2014 20/12/2014",
        )
        # allow following tests to reuse the same XML file
        invoices[0].ref = invoices[0].payment_reference = "14381"
        invoices[1].ref = invoices[1].payment_reference = "14382"

    def test_40_xml_import_withholding(self):
        res = self.run_wizard("test40", "IT01234567890_FPR11.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains ImportoRitenuta 92.0 but created invoice has got "
            "144.0\n.",
        )

    def test_41_xml_import_withholding(self):
        res = self.run_wizard("test41", "IT01234567890_FPR12.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 2)
        self.assertAlmostEqual(invoice.amount_total, 1220.0)
        self.assertAlmostEqual(invoice.withholding_tax_amount, 94.0)
        self.assertAlmostEqual(invoice.amount_net_pay, 1126.0)

    def test_42_xml_import_withholding(self):
        # cassa previdenziale sulla quale è applicata la ritenuta
        res = self.run_wizard("test42", "IT01234567890_FPR13.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_total, 19032.0)
        self.assertEqual(invoice.withholding_tax_amount, 3120.0)
        self.assertEqual(invoice.amount_net_pay, 15912.0)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 1)
        self.assertTrue(len(invoice.invoice_line_ids) == 2)

    def test_43_xml_import_withholding(self):
        # Avvocato Mario Bianchi di Ferrara.
        # Imponibile di 100+15% spese
        res = self.run_wizard("test43", "ITBNCMRA80A01D548T_20001.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.withholding_tax_amount, 23.0)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 1)
        self.assertTrue(len(invoice.invoice_line_ids) == 3)

    def test_44_xml_import(self):
        res = self.run_wizard("test44", "ITBNCMRA80A01D548T_20005.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.invoice_line_ids) == 3)

    def test_45_xml_import_no_duplicate_partner(self):
        partner_id = self.env["res.partner"].search([("vat", "ilike", "05979361218")])
        if not partner_id:
            # load bill (when this test is run by itself)
            res = self.run_wizard("test45a", "IT05979361218_001.xml")
            partner_id = self.env["res.partner"].search(
                [("vat", "ilike", "05979361218")]
            )
            # allow following code to reuse the same XML file
            invoice_id = res.get("domain")[0][2][0]
            invoice = self.invoice_model.browse(invoice_id)
            invoice.ref = invoice.payment_reference = "14451"

        # try and alter the vat of the existing partner
        partner_id.write({"vat": " %s  " % partner_id.vat})

        # load bill (2nd time)
        res = self.run_wizard("test45b", "IT05979361218_001.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        # check for duplicates
        self.assertEqual(invoice.partner_id.id, partner_id.id)
        self.assertEqual(
            len(self.env["res.partner"].search([("vat", "ilike", "05979361218")])), 1
        )

    def test_46_xml_many_zeros(self):
        res = self.run_wizard("test46", "IT05979361218_016.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_total, 18.07)
        self.assertAlmostEqual(invoice.invoice_line_ids[0].price_unit, 18.07)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 1.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 18.07)
        self.assertAlmostEqual(invoice.invoice_line_ids[1].price_unit, 16.60)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1.0)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, 0.0)

    def test_47_xml_import(self):
        res = self.run_wizard("test47", "IT01234567890_FPR14.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertTrue(
            "Untaxed amount (44480.0) does not match with e-bill untaxed amount "
            "(44519.26)" in invoice.e_invoice_validation_message
        )
        # Due to multiple SQL transactions, we cannot test the correct importation.
        # IT01234567890_FPR14.xml should be tested manually

    def test_48_xml_import(self):
        # my company bank account is the same as the one in XML:
        # invoice creation must not be blocked
        self.env["res.partner.bank"].create(
            {
                "acc_number": "IT59R0100003228000000000622",
                "company_id": self.env.company.id,
                "partner_id": self.env.company.partner_id.id,
            }
        )
        res = self.run_wizard("test48", "IT01234567890_FPR15.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(
            "Bank account IT59R0100003228000000000622 already exists"
            in invoice.inconsistencies
        )

    def test_49_xml_import(self):
        # this method name is used in 12.0
        # reserving to make forward-porting easier
        pass

    def test_50_xml_import(self):
        """
        Check that products can be found using "Vendor Product Name".
        """
        partner_id = self.env["res.partner"].name_search("SOCIETA' ALPHA SRL")[0][0]
        product_id = self.env["product.product"].name_create(
            "Test supplier description"
        )[0]
        self.env["product.supplierinfo"].create(
            {
                "name": partner_id,
                "product_name": "FORNITURE VARIE PER UFFICIO",
                "product_id": product_id,
                "min_qty": 1,
                "price": 100,
            }
        )

        res = self.run_wizard("test50", "IT01234567890_FPR03.xml")
        invoice_ids = res.get("domain")[0][2]
        invoice = self.invoice_model.browse(invoice_ids).filtered(
            lambda x: x.ref == "123"
        )
        self.assertEqual(len(invoice), 1)
        invoice_line = invoice.invoice_line_ids.filtered(
            lambda l: l.product_id.id == product_id
        )
        self.assertEqual(len(invoice_line), 1)

        # allow following tests to reuse the same XML file
        invoice.ref = invoice.payment_reference = "14501"

    def test_51_xml_import(self):
        res = self.run_wizard("test51", "IT02780790107_11008.xml")
        invoice_ids = res.get("domain")[0][2]
        invoice = self.invoice_model.browse(invoice_ids)
        self.assertTrue(invoice.fatturapa_attachment_in_id.is_self_invoice)

    def test_52_12_xml_import(self):
        """
        Check that an XML with syntax error is created,
        but it shows a parsing error.
        """
        with mute_logger("odoo.addons.l10n_it_fatturapa_in.models.attachment"):
            attachment = self.create_attachment(
                "test52_12",
                "ZGEXQROO37831_anonimizzata.xml",
            )
        self.assertIn(
            "Impossible to parse XML for test52_12:",
            attachment.e_invoice_parsing_error or "",
        )

    def test_52_xml_import(self):
        # we test partner creation, too
        # make sure a partner with the same vat is already in the DB
        for partner in self.env["res.partner"].search([("vat", "=", "IT02780790107")]):
            # references from aml may prevent partner unlinking
            self.env["account.move.line"].search(
                [("partner_id", "=", partner.id)]
            ).unlink()
            self.env["account.move"].search([("partner_id", "=", partner.id)]).unlink()
            partner.unlink()

        res = self.run_wizard("test52", "IT02780790107_11009.xml")
        invoice_ids = res.get("domain")[0][2]
        invoice = self.invoice_model.browse(invoice_ids)

        self.assertEqual(len(invoice.e_invoice_line_ids), 1)
        self.assertEqual(invoice.e_invoice_line_ids[0].tax_kind, "N4")

        self.assertEqual(len(invoice.invoice_line_ids), 1)
        self.assertEqual(len(invoice.invoice_line_ids[0].tax_ids), 1)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 272.23)
        kind = self.env.ref("l10n_it_account_tax_kind.n4")
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids[0].kind_id, kind)

        self.assertEqual(invoice.amount_total, 272.23)

        self.assertTrue(invoice.partner_id)
        self.assertEqual(invoice.partner_id.firstname, "Mario")
        self.assertEqual(invoice.partner_id.lastname, "Rossi")

    def test_53_xml_import(self):
        """
        Check that VAT of non-IT partner is not checked.
        """
        partner_model = self.env["res.partner"]
        # Arrange: A partner with vat GB99999999999 does not exist
        not_valid_vat = "GB99999999999"

        def vat_partner_exists():
            return partner_model.search(
                [
                    ("vat", "=", not_valid_vat),
                ]
            )

        self.assertFalse(vat_partner_exists())

        # Act: Import an e-bill containing a supplier with vat GB99999999999
        self.create_attachment(
            "test53",
            "IT01234567890_x05mX.xml",
        )

        # Assert: A partner with vat GB99999999999 exists,
        # and the vat is usually not valid for UK
        self.assertTrue(vat_partner_exists())
        with self.assertRaises(ValidationError) as ve:
            partner_model.create(
                [
                    {
                        "name": "Test not valid VAT",
                        "country_id": self.ref("base.uk"),
                        "vat": not_valid_vat,
                    }
                ]
            )
        exc_message = ve.exception.args[0]
        self.assertRegex(
            exc_message,
            "VAT number .*{not_valid_vat}.* does not seem to be valid".format(
                not_valid_vat=not_valid_vat,
            ),
        )

    def test_54_xml_import(self):
        """
        Test: Negative invoice (TD01) is correctly imported,
        converted all values to positive and set move_type to in_refund
        """
        res = self.run_wizard("test54", "IT02098391200_FPR16.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_untaxed, 1.5)
        self.assertEqual(invoice.amount_total, 1.83)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 0.15)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 10.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 1.5)
        self.assertEqual(invoice.move_type, "in_refund")

    def test_01_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are kept.
        """

        supplier = self.env["res.partner"].search(
            [("vat", "=", "IT02780790107")], limit=1
        )
        invoice_form = Form(
            self.invoice_model.with_context(default_move_type="in_invoice")
        )
        invoice_form.partner_id = supplier
        invoice_form.ref = "original_ref"
        invoice_form.payment_reference = "original_ref"
        invoice_form.invoice_date = date(2020, 1, 1)
        orig_invoice = invoice_form.save()
        wizard_line_form = Form(self.wizard_link_inv_line_model)
        wizard_line_form.invoice_id = orig_invoice
        line_id = wizard_line_form.save()
        self.run_wizard(
            "test_link_01",
            "IT01234567890_FPR04.xml",
            mode="link",
            wiz_values=line_id,
        )
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice_form.ref,
            orig_invoice.ref,
        )
        self.assertEqual(
            invoice_form.payment_reference,
            orig_invoice.payment_reference,
        )

    def test_02_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are fetched from the XML.
        """

        supplier = self.env["res.partner"].search(
            [("vat", "=", "IT02780790107")], limit=1
        )
        invoice_form = Form(
            self.invoice_model.with_context(default_move_type="in_invoice")
        )
        invoice_form.partner_id = supplier
        orig_invoice = invoice_form.save()
        wizard_line_form = Form(self.wizard_link_inv_line_model)
        wizard_line_form.invoice_id = orig_invoice
        line_id = wizard_line_form.save()
        self.run_wizard(
            "test_link_02",
            "IT02780790107_11004.xml",
            mode="link",
            wiz_values=line_id,
        )
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertTrue(orig_invoice.ref)
        self.assertTrue(orig_invoice.payment_reference)
        self.assertTrue(orig_invoice.invoice_date)
        # allow following tests to reuse the same XML file
        orig_invoice.ref = orig_invoice.payment_reference = "14021"

    def test_01_xml_preview(self):
        res = self.run_wizard("test_preview", "IT05979361218_001.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        preview_action = invoice.fatturapa_attachment_in_id.ftpa_preview()
        self.assertEqual(
            preview_action["url"], invoice.fatturapa_attachment_in_id.ftpa_preview_link
        )

    def test_01_xml_zero_quantity_line(self):
        res = self.run_wizard("test_zeroq_01", "IT05979361218_q0.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 0)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1)

    def test_xml_import_summary_tax_rate(self):
        # Invoice  with positive total. Detail Level:  '1' -- Tax Rate
        supplier = self.env["res.partner"].search([("vat", "=", "IT02780790107")])[0]
        # in order to make the system create the invoice lines
        supplier.e_invoice_detail_level = "1"
        res = self.run_wizard("test_summary_tax_rate", "IT05979361218_ripilogoiva.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_total, 204.16)
        self.assertEqual(len(invoice.invoice_line_ids), 2)

        self.assertAlmostEqual(invoice.invoice_line_ids[0].price_unit, 164.46)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 1.0)
        self.assertAlmostEqual(invoice.invoice_line_ids[1].price_unit, 3.52)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1.0)

    def test_e_invoice_field_compute(self):
        """Check successful creation of multiple invoices.
        See https://github.com/OCA/l10n-italy/issues/2349"""
        invoices = self.invoice_model.create([{}, {}])
        self.assertEqual(invoices.mapped("e_invoice_validation_error"), [False, False])

    def test_duplicated_vat_on_partners(self):
        supplier = self.env["res.partner"].search(
            [("vat", "=", "IT05979361218")], limit=1
        )

        duplicated_supplier = supplier.copy()
        self.assertEqual(supplier.vat, duplicated_supplier.vat)
        attach = self.run_wizard("duplicated_vat", "IT05979361218_012.xml", mode=False)
        self.assertFalse(attach.xml_supplier_id)
        self.assertTrue(attach.inconsistencies)

    def test_access_other_user_e_invoice(self):
        """A user can see the e-invoice files created by other users."""
        # Arrange
        access_right_group_xmlid = "base.group_erp_manager"
        user = self.env.user
        user.groups_id -= self.env.ref("base.group_system")
        user.groups_id -= self.env.ref(access_right_group_xmlid)
        other_user = self.env["res.users"].create(
            {
                "name": "Other User",
                "login": "other.user@example.org",
                "groups_id": [(6, 0, user.groups_id.ids)],
            }
        )
        # pre-condition
        self.assertFalse(user.has_group(access_right_group_xmlid))
        self.assertNotEqual(user, other_user)

        # Act
        with self.with_user(other_user.login):
            import_action = self.run_wizard(
                "access_other_user_e_invoice", "IT01234567890_FPR03.xml"
            )

        # Assert
        invoices = self.env[import_action["res_model"]].search(import_action["domain"])
        e_invoice = invoices.fatturapa_attachment_in_id
        self.assertTrue(e_invoice.ir_attachment_id.read())


class TestFatturaPAEnasarco(FatturapaCommon):
    def setUp(self):
        super(TestFatturaPAEnasarco, self).setUp()

        self.invoice_model = self.env["account.move"]

    def test_01_xml_import_enasarco(self):
        self.create_wt_enasarco_157_r()
        self.create_wt_enasarco_85_r()
        self.create_wt_enasarco_115_a()
        self.create_wt_115_r()
        # case with ENASARCO only in DatiCassaPrevidenziale and not in DatiRitenuta.
        # This should not happen, but it is valid for SDI
        res = self.run_wizard("test01", "IT05979361218_014.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.amount_untaxed, 2470.00)
        self.assertEqual(invoice.amount_tax, 543.40)
        self.assertEqual(invoice.amount_total, 3013.40)
        self.assertEqual(invoice.amount_net_pay, 2729.35)
        self.assertEqual(invoice.withholding_tax_amount, 284.05)
        self.assertEqual(invoice.welfare_fund_ids[0].kind_id.code, "N2")
        self.assertTrue(len(invoice.e_invoice_line_ids) == 1)
        self.assertEqual(invoice.e_invoice_line_ids[0].name, "ACCONTO PROVVIGIONI")
        self.assertEqual(invoice.e_invoice_line_ids[0].qty, 1.0)
        self.assertEqual(invoice.e_invoice_line_ids[0].unit_price, 2470.0)
        self.assertEqual(invoice.e_invoice_line_ids[0].total_price, 2470.0)

    def test_02_xml_import_enasarco(self):
        # Giacomo Neri, agente di commercio di Firenze.
        # Imponibile 10
        res = self.run_wizard("test02", "ITNREGCM80H30D612D_20003.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_untaxed, 10.0)
        self.assertEqual(invoice.amount_tax, 2.2)
        self.assertEqual(round(invoice.amount_total, 2), 12.2)
        self.assertEqual(round(invoice.amount_net_pay, 2), 10.2)
        self.assertTrue(len(invoice.invoice_line_ids) == 1)

    def test_03_xml_import_enasarco(self):
        # Come sopra, ma senza "<Ritenuta>SI</Ritenuta>" in riga fattura
        res = self.run_wizard("test03", "ITNREGCM80H30D612D_20004.xml")
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(
            "E-bill contains DatiRitenuta but no lines subjected to Ritenuta was found"
            in invoice.e_invoice_validation_message
        )
        self.assertEqual(round(invoice.amount_total, 2), 12.2)
        self.assertEqual(round(invoice.amount_net_pay, 2), 12.2)
