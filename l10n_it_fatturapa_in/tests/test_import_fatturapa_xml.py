from psycopg2 import IntegrityError

from datetime import date

from odoo.tools import mute_logger
from .fatturapa_common import FatturapaCommon
from odoo.exceptions import UserError


class TestDuplicatedAttachment(FatturapaCommon):

    def test_duplicated_attachment(self):
        """Attachment name must be unique"""
        # This test breaks the current transaction
        # and every test executed after this in the
        # same transaction would fail.
        # Note that all the tests in TestFatturaPAXMLValidation
        # are executed in the same transaction.
        self.run_wizard('test_duplicated', 'IT02780790107_11005.xml')
        with self.assertRaises(IntegrityError) as ie:
            with mute_logger('odoo.sql_db'):
                self.run_wizard('test_duplicated', 'IT02780790107_11005.xml')
        self.assertEqual(ie.exception.pgcode, '23505')


class TestFatturaPAXMLValidation(FatturapaCommon):

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()

    def test_00_xml_import(self):
        self.env.user.company_id.cassa_previdenziale_product_id = (
            self.service.id)
        res = self.run_wizard('test0', 'IT05979361218_001.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.register_code, 'TO1258B')
        self.assertEqual(
            invoice.partner_id.register_fiscalpos.code, 'RF02')
        self.assertEqual(invoice.reference, 'FT/2015/0006')
        self.assertEqual(invoice.amount_total, 57.00)
        self.assertEqual(invoice.gross_weight, 0.00)
        self.assertEqual(invoice.net_weight, 0.00)
        self.assertEqual(invoice.welfare_fund_ids[0].kind_id.code, 'N4')
        self.assertFalse(invoice.art73)
        welfare_found = False
        for line in invoice.invoice_line_ids:
            if line.product_id.id == self.service.id:
                self.assertEqual(line.price_unit, 3)
                welfare_found = True
        self.assertTrue(welfare_found)
        self.assertTrue(len(invoice.e_invoice_line_ids) == 1)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].name, 'Prodotto di test al giorno')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].qty, 15)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].uom, 'Giorno(i)')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].unit_price, 3.6)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].total_price, 54)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].tax_amount, 0)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].tax_kind, 'N4')
        self.assertTrue(len(invoice.e_invoice_line_ids[0].other_data_ids) == 2)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].other_data_ids[0].text_ref,
            'Riferimento')

    def test_01_xml_import(self):
        res = self.run_wizard('test1', 'IT02780790107_11004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, '123')
        self.assertEqual(invoice.amount_untaxed, 34.00)
        self.assertEqual(invoice.amount_tax, 7.48)
        self.assertEqual(
            len(invoice.invoice_line_ids[0].invoice_line_tax_ids), 1)
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name,
            '22% e-bill')
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_untaxed, 34.00)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_tax, 7.48)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].payability, 'D')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(invoice.partner_id.state_id.code, "SS")
        self.assertEqual(invoice.partner_id.country_id.code, "IT")
        self.assertEqual(
            invoice.tax_representative_id.name, "Rappresentante fiscale")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_rate_tax, 0.04)
        order_related_doc = invoice.related_documents.filtered(
            lambda rd: rd.type == 'order'
        )
        self.assertTrue(order_related_doc)
        self.assertEqual(order_related_doc.cig, '456def')
        self.assertEqual(order_related_doc.cup, '123abc')
        self.assertEqual(
            invoice.welfare_fund_ids[0].welfare_amount_tax, 9)
        self.assertFalse(invoice.welfare_fund_ids[0].welfare_taxable)
        self.assertEqual(invoice.unit_weight, 'KGM')
        self.assertEqual(invoice.ftpa_incoterms, 'DAP')
        self.assertEqual(invoice.fiscal_document_type_id.code, 'TD01')
        self.assertTrue(invoice.art73)

    def test_02_xml_import(self):
        res = self.run_wizard('test02', 'IT05979361218_011.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.intermediary.vat, 'IT03339130126')

    # def test_02_xml_import(self):
    #     res = self.run_wizard('test2', 'IT03638121008_X11111.xml')
    #     invoice_id = res.get('domain')[0][2][0]
    #     invoice = self.invoice_model.browse(invoice_id)
    #     self.assertEqual(invoice.supplier_invoice_number, '00001')
    #     self.assertEqual(invoice.amount_untaxed, 3)
    #     self.assertEqual(invoice.amount_tax, 0.66)
    #     self.assertEqual(
    #         invoice.fatturapa_summary_ids[0].amount_untaxed, 3)
    #     self.assertEqual(
    #         invoice.fatturapa_summary_ids[0].amount_tax, 0.66)
    #     self.assertEqual(invoice.partner_id.name, "Societa' alpha S.r.l.")

    def test_04_xml_import(self):
        res = self.run_wizard('test4', 'IT02780790107_11005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, '124')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name,
            '22% e-bill')
        self.assertEqual(
            invoice.invoice_line_ids[1].invoice_line_tax_ids[0].name,
            '22% e-bill')
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].amount, 22)
        self.assertEqual(
            invoice.invoice_line_ids[1].invoice_line_tax_ids[0].amount, 22)
        self.assertEqual(
            invoice.invoice_line_ids[1].price_unit, 2)
        self.assertTrue(len(invoice.e_invoice_line_ids) == 2)
        for e_line in invoice.e_invoice_line_ids:
            self.assertTrue(e_line.line_number in (1, 2))
            if e_line.line_number == 1:
                self.assertEqual(
                    e_line.cod_article_ids[0].name, 'EAN')
                self.assertEqual(
                    e_line.cod_article_ids[0].code_val, '12345')
        self.assertEqual(
            invoice.inconsistencies,
            u"Company Name field contains 'Societa\' "
            u"Alpha SRL'. Your System contains 'SOCIETA\' ALPHA SRL'\n\n")

    def test_05_xml_import(self):
        res = self.run_wizard('test5', 'IT05979361218_003.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0008')
        self.assertEqual(invoice.sender, 'TZ')
        self.assertEqual(invoice.intermediary.name, 'MARIO ROSSI')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].name,
            'SC')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].
            percentage, 10
        )
        self.assertEqual(invoice.amount_untaxed, 9)
        self.assertEqual(invoice.amount_tax, 0)
        self.assertEqual(invoice.amount_total, 9)

    def test_06_import_except(self):
        # File not exist Exception
        self.assertRaises(
            Exception, self.run_wizard, 'test6_Exception', '')
        # fake Signed file is passed , generate orm_exception
        self.assertRaises(
            UserError, self.run_wizard, 'test6_orm_exception',
            'IT05979361218_fake.xml.p7m'
        )

    def test_07_xml_import(self):
        # 2 lines with quantity != 1 and discounts
        res = self.run_wizard('test7', 'IT05979361218_004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0009')
        self.assertAlmostEqual(invoice.amount_untaxed, 1173.60)
        self.assertEqual(invoice.amount_tax, 258.19)
        self.assertEqual(invoice.amount_total, 1431.79)
        self.assertAlmostEqual(
            invoice.e_invoice_amount_untaxed, invoice.amount_untaxed,
            places=invoice.currency_id.decimal_places)
        self.assertAlmostEqual(
            invoice.e_invoice_amount_tax, invoice.amount_tax,
            places=invoice.currency_id.decimal_places)
        self.assertEqual(invoice.e_invoice_validation_error, False)
        self.assertEqual(invoice.invoice_line_ids[0].admin_ref, 'D122353')

    def test_08_xml_import(self):
        # using ImportoTotaleDocumento
        res = self.run_wizard('test8', 'IT05979361218_005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0010')
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertFalse(invoice.inconsistencies)

    def test_09_xml_import(self):
        # using DatiGeneraliDocumento.ScontoMaggiorazione without
        # ImportoTotaleDocumento
        # add test file name case sensitive
        res = self.run_wizard('test9', 'IT05979361218_006.XML')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0011')
        self.assertAlmostEqual(invoice.amount_total, 1288.61)
        self.assertEqual(
            invoice.inconsistencies,
            'Computed amount untaxed 1030.42 is different from'
            ' summary data 1173.6')

    def test_10_xml_import(self):
        # Fix Date format
        res = self.run_wizard('test6', 'IT05979361218_007.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0009')
        self.assertEqual(
            invoice.date_invoice, date(2015, 3, 16))
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_due_date,
            date(2015, 6, 3)
        )
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].
            fatturapa_pm_id.code,
            'MP18'
        )

    def test_11_xml_import(self):
        # DatiOrdineAcquisto with RiferimentoNumeroLinea referring to
        # not existing invoice line
        res = self.run_wizard('test11', 'IT02780790107_11006.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(
            len(invoice.invoice_line_ids[0].related_documents), 0)
        self.assertEqual(
            invoice.invoice_line_ids[0].sequence, 1)
        self.assertEqual(
            invoice.related_documents[0].type, "order")
        self.assertEqual(
            invoice.related_documents[0].lineRef, 60)

    def test_12_xml_import(self):
        res = self.run_wizard('test12', 'IT05979361218_008.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0012')
        self.assertEqual(invoice.sender, 'TZ')
        self.assertEqual(invoice.intermediary.name, 'MARIO ROSSI')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')

    def test_13_xml_import(self):
        # inconsistencies must not be duplicated
        res = self.run_wizard_multi([
            'IT02780790107_11005.xml',
            'IT02780790107_11006.xml',
            ])
        invoice1_id = res.get('domain')[0][2][0]
        invoice2_id = res.get('domain')[0][2][1]
        invoice1 = self.invoice_model.browse(invoice1_id)
        invoice2 = self.invoice_model.browse(invoice2_id)
        self.assertEqual(
            invoice1.inconsistencies,
            u"Company Name field contains 'Societa\' "
            u"Alpha SRL'. Your System contains 'SOCIETA\' ALPHA SRL'\n\n")
        self.assertEqual(
            invoice2.inconsistencies,
            u"Company Name field contains 'Societa\' "
            u"Alpha SRL'. Your System contains 'SOCIETA\' ALPHA SRL'\n\n")

    def test_14_xml_import(self):
        # check: no tax code found , write inconsisteance and anyway
        # create draft
        res = self.run_wizard('test14', 'IT02780790107_11007.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, '136')
        self.assertEqual(invoice.partner_id.name, 'SOCIETA\' ALPHA SRL')
        self.assertEqual(invoice.amount_untaxed, 25.00)
        self.assertEqual(invoice.amount_tax, 0.0)
        self.assertEqual(
            invoice.inconsistencies,
            u"Company Name field contains 'Societa\' "
            "Alpha SRL'. Your System contains 'SOCIETA\' ALPHA SRL'\n\n"
            u"XML contains tax with percentage '15.55'"
            " but it does not exist in your system\n"
            "XML contains tax with percentage '15.55'"
            " but it does not exist in your system")

    def test_15_xml_import(self):
        self.wt = self.create_wt()
        res = self.run_wizard('test15', 'IT05979361218_009.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEquals(invoice.withholding_tax_amount, 1)
        self.assertAlmostEquals(invoice.amount_total, 6.1)
        self.assertAlmostEquals(invoice.amount_net_pay, 5.1)

    def test_16_xml_import(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        res = self.run_wizard('test16a', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, '')
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertTrue(len(invoice.invoice_line_ids) == 2)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)
            if invoice.reference == '456':
                self.assertTrue(len(invoice.invoice_line_ids) == 1)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)

        partner = invoice.partner_id
        partner.e_invoice_default_product_id = (
            self.imac.product_variant_ids[0].id)
        # I create a supplier code to be matched in XML
        self.env['product.supplierinfo'].create({
            'name': partner.id,
            'product_tmpl_id': self.headphones.id,
            'product_code': 'ART123',
        })
        res = self.run_wizard('test16b', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        for invoice in invoices:
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertEqual(
                    invoice.invoice_line_ids[0].product_id.id,
                    self.headphones.product_variant_ids[0].id
                )
            else:
                for line in invoice.invoice_line_ids:
                    self.assertEqual(
                        line.product_id.id,
                        self.imac.product_variant_ids[0].id
                    )

        # change Livello di dettaglio Fatture elettroniche to Minimo
        partner.e_invoice_detail_level = '0'
        res = self.run_wizard('test16c', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertTrue(len(invoices) == 2)
        for invoice in invoices:
            self.assertTrue(len(invoice.invoice_line_ids) == 0)

    def test_03_xml_import(self):
        # Testing CAdES signature
        res = self.run_wizard('test18', 'IT01234567890_FPR03.xml.p7m')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, '')
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertTrue(len(invoice.invoice_line_ids) == 2)
            if invoice.reference == '456':
                self.assertTrue(len(invoice.invoice_line_ids) == 1)

    def test_17_xml_import(self):
        res = self.run_wizard('test17', 'IT05979361218_010.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(
            invoice.related_documents[0].type, "invoice")

    def test_19_xml_import(self):
        # Testing CAdES signature, base64 encoded
        res = self.run_wizard(
            'test19', 'IT01234567890_FPR03.base64.xml.p7m',
            'IT01234567890_FPR03.xml.p7m')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertEqual(invoice.partner_id.e_invoice_detail_level, '0')
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertEqual(
                    invoice.inconsistencies,
                    'Computed amount untaxed 0.0 is different from summary '
                    'data 25.0')
            if invoice.reference == '456':
                self.assertEqual(
                    invoice.inconsistencies,
                    'Computed amount untaxed 0.0 is different from summary '
                    'data 2000.0')

    def test_20_xml_import(self):
        # Testing xml without xml declaration (sent by Amazon)
        res = self.run_wizard('test20', 'IT05979361218_no_decl.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

    def test_21_xml_import(self):
        supplier = self.env['res.partner'].search(
            [('vat', '=', 'IT02780790107')])[0]
        # in order to make the system create the invoice lines
        supplier.e_invoice_detail_level = '2'
        res = self.run_wizard('test21', 'IT01234567890_FPR04.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.inconsistencies, '')
        self.assertEqual(invoice.invoice_line_ids[2].price_unit, 0.0)
        self.assertEqual(invoice.invoice_line_ids[2].discount, 0.0)

    def test_22_xml_import(self):
        res = self.run_wizard('test22', 'IT02780790107_11004_xml_doctor.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")

        self.assertIn('removed timezone information', invoice.inconsistencies)

        # DatiGeneraliDocumento/Causale
        self.assertIn(' ', invoice.comment)

        # DatiGeneraliDocumento/Data
        self.assertEqual(invoice.date_invoice, date(2014, 12, 18))

        # DatiTrasporto/IndirizzoResa/NumeroCivico
        self.assertEqual(invoice.delivery_address,
                         'strada dei test,  \n12042 - Bra\nCN IT')

        # DatiTrasporto/DataOraConsegna
        self.assertFalse(invoice.delivery_datetime)

        # DatiBeniServizi/DettaglioLinee/Descrizione
        self.assertEqual(invoice.invoice_line_ids[0].name, ' ')

        # DatiPagamento/DettaglioPagamento/DataDecorrenzaPenale
        payment_data = self.env['fatturapa.payment.data'].search(
            [('invoice_id', '=', invoice.id)])
        self.assertEqual(payment_data[0].payment_methods[0].penalty_date,
                         date(2015, 5, 1))

    def test_23_xml_import(self):
        # Testing CAdES signature, base64 encoded with newlines
        res = self.run_wizard(
            'test23', 'IT01234567890_FPR04.base64.xml.p7m',
            'IT01234567890_FPR04.xml.p7m')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)

    def test_24_xml_import(self):
        res = self.run_wizard('test24', 'IT05979361218_012.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.32)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)

    def test_25_xml_import(self):
        res = self.run_wizard('test25', 'IT05979361218_013.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.32)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)

    def test_30_xml_import(self):
        self.env.user.company_id.cassa_previdenziale_product_id = (
            self.service.id)
        res = self.run_wizard('test30', 'IT05979361218_001.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        partner_id = invoice.partner_id
        partner_id.write({
            'street': 'Viale Repubblica, 34',
            'electronic_invoice_no_contact_update': True,
        })
        res = self.run_wizard('test30a', 'IT05979361218_002.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.id, partner_id.id)
        self.assertEqual(invoice.partner_id.street, 'Viale Repubblica, 34')

    def test_31_xml_import(self):
        res = self.run_wizard('test31', 'IT01234567890_FPR05.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[1].discount, 100)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, 0)
        self.assertEqual(invoice.amount_total, 12.2)

    def test_01_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are kept.
        """

        supplier = self.env['res.partner'].search(
            [('vat', '=', 'IT02780790107')], limit=1)
        invoice_values = {
            'partner_id': supplier.id,
            'type': 'in_invoice',
            'reference': 'original_ref',
            'date_invoice': date(2020, 1, 1),
        }
        orig_invoice = self.invoice_model.create(invoice_values)
        wiz_values = {
            'line_ids': [(0, 0, {
                'invoice_id': orig_invoice.id
            })],
        }
        self.run_wizard('test_link_01', 'IT01234567890_FPR04.xml',
                        mode='link', wiz_values=wiz_values)
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice_values['reference'],
            orig_invoice.reference,
        )
        self.assertEqual(
            invoice_values['date_invoice'],
            orig_invoice.date_invoice,
        )

    def test_02_xml_link(self):
        """
        E-invoice lines are created.
        Vendor Reference and Invoice Date are fetched from the XML.
        """

        supplier = self.env['res.partner'].search(
            [('vat', '=', 'IT02780790107')], limit=1)
        invoice_values = {
            'partner_id': supplier.id,
            'type': 'in_invoice',
        }
        orig_invoice = self.invoice_model.create(invoice_values)
        wiz_values = {
            'line_ids': [(0, 0, {
                'invoice_id': orig_invoice.id
            })],
        }
        self.run_wizard('test_link_02', 'IT02780790107_11004.xml',
                        mode='link', wiz_values=wiz_values)
        self.assertTrue(orig_invoice.e_invoice_line_ids)
        self.assertFalse(orig_invoice.invoice_line_ids)
        self.assertTrue(orig_invoice.e_invoice_validation_error)
        self.assertTrue(orig_invoice.reference)
        self.assertTrue(orig_invoice.date_invoice)
