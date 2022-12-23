from psycopg2 import IntegrityError

from datetime import date

from odoo.tools import mute_logger
from .fatturapa_common import FatturapaCommon
from odoo.exceptions import UserError, ValidationError


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
        self.wt = self.create_wt_4q()
        self.wtq = self.create_wt_27_20q()
        self.wt4q = self.create_wt_26_40q()
        self.wt2q = self.create_wt_26_20q()
        self.invoice_model = self.env['account.invoice']

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
        self.assertEqual(invoice.partner_id.vat, "IT02780790107")
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
        # fake Signed file is passed , generate parsing error
        attachment = self.create_attachment(
            'test6_orm_exception', 'IT05979361218_fake.xml.p7m')
        self.assertIn('Invalid xml', attachment.e_invoice_parsing_error)

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

    def test_08_xml_import_no_account(self):
        """Check that a useful error message is raised when
        the credit account is missing in purchase journal."""
        company = self.env.user.company_id
        journal = self.wizard_model.get_purchase_journal(company)
        journal_credit_account = journal.default_credit_account_id
        journal.default_credit_account_id = False

        expense_default_property = self.env['ir.property']._get_property(
            'property_account_expense_categ_id',
            'product.category',
            res_id=False,
        )
        # Setting res_id disables the property from acting as default value
        expense_default_property.res_id = 1
        with self.assertRaises(UserError) as ue:
            self.run_wizard('test8_no_account', 'IT05979361218_005.xml')
        self.assertIn(journal.display_name, ue.exception.name)
        self.assertIn(company.display_name, ue.exception.name)

        discount_amount = -143.18
        # Restore the property and import the invoice
        expense_default_property.res_id = False
        res = self.run_wizard('test8_with_property', 'IT05979361218_005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        invoice_lines = invoice.invoice_line_ids
        discount_line = invoice_lines.filtered(
            lambda line: line.price_unit == discount_amount)
        self.assertEqual(
            discount_line.account_id,
            expense_default_property.get_by_record(),
        )

        # Restore the journal's account and import the invoice
        journal.default_credit_account_id = journal_credit_account
        res = self.run_wizard('test8_with_journal', 'IT05979361218_005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        invoice_lines = invoice.invoice_line_ids
        discount_line = invoice_lines.filtered(
            lambda line: line.price_unit == discount_amount)
        self.assertEqual(
            discount_line.account_id,
            journal_credit_account,
        )
        self.assertTrue(invoice)

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
                self.assertEqual(invoice.date_due, date(2015, 1, 30))
            if invoice.reference == '456':
                self.assertTrue(len(invoice.invoice_line_ids) == 1)
                for line in invoice.invoice_line_ids:
                    self.assertFalse(line.product_id)
                self.assertEqual(invoice.date_due, date(2015, 1, 28))

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
        self.assertEqual(
            invoice.inconsistencies,
            'Computed amount untaxed 34.32 is different from'
            ' summary data 34.67')

    def test_25_xml_import(self):
        res = self.run_wizard('test25', 'IT05979361218_013.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.67)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)
        self.assertEqual(invoice.efatt_rounding, -0.35)
        invoice.action_invoice_open()
        move_line = False
        for line in invoice.move_id.line_ids:
            if line.account_id.id == self.env.user.\
                    company_id.arrotondamenti_attivi_account_id.id:
                move_line = True
        self.assertTrue(move_line)

        # Update the reference so that importing the same file
        # (in other tests) does not raise "Duplicated vendor reference..."
        invoice.reference = 'test25'

    def test_26_xml_import(self):
        res = self.run_wizard('test26', 'IT05979361218_015.xml')
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

    def test_32_xml_import(self):
        # Refund with positive total
        res = self.run_wizard('test32', 'IT01234567890_FPR06.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.type, 'in_refund')
        self.assertEqual(invoice.amount_total, 18.3)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 2.0)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 10.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 20.0)
        self.assertEqual(invoice.invoice_line_ids[1].price_unit, -1.0)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 5.0)
        self.assertEqual(invoice.invoice_line_ids[1].price_subtotal, -5.0)

    def test_33_xml_import(self):
        # Refund with negative total
        res = self.run_wizard('test33', 'IT01234567890_FPR07.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.type, 'in_refund')
        self.assertEqual(invoice.amount_total, 24.4)
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 2.0)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 10.0)
        self.assertEqual(invoice.invoice_line_ids[0].price_subtotal, 20.0)
        self.assertEqual(invoice.e_invoice_amount_untaxed, -20.0)
        self.assertEqual(invoice.e_invoice_amount_tax, -4.4)

    def test_34_xml_import(self):
        # No Ritenuta lines set
        res = self.run_wizard('test34', 'IT01234567890_FPR08.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains DatiRitenuta but no lines subjected to Ritenuta was "
            "found. Please manually check Withholding tax Amount\nE-bill contains "
            "ImportoRitenuta 360.0 but created invoice has got 0.0\n."
        )

    def test_35_xml_import(self):
        # creating 2350 before 2320, so odoo will use 2350 but e-invoices
        # contains 2320: error message must appear
        self.create_wt_23_50()
        self.create_wt_23_20()
        res = self.run_wizard('test35', 'IT01234567890_FPR09.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains ImportoRitenuta 30.16 but created invoice has got "
            "75.41\n."
        )

    def test_36_xml_import(self):
        # creating a res.bank and importing an XML without "IstitutoFinanziario"
        self.create_res_bank()
        res = self.run_wizard('test36', 'IT01234567890_FPR10.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_bank.bank_id.bic,
            'BCITITMM')
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_bank.bank_id.name,
            'Banca generica')

    def test_37_xml_import_dates(self):
        self.env.user.lang = 'it_IT'
        res = self.run_wizard('test37', 'IT02780790107_11004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.fatturapa_attachment_in_id.invoices_date,
                         '18/12/2014')

    def test_38_xml_import_dates(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        self.env.user.lang = 'it_IT'
        res = self.run_wizard('test38', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        self.assertEqual(invoices[0].fatturapa_attachment_in_id.invoices_date,
                         '18/12/2014 20/12/2014')

    def test_40_xml_import_withholding(self):
        res = self.run_wizard('test40', 'IT01234567890_FPR11.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertEqual(
            invoice.e_invoice_validation_message,
            "E-bill contains ImportoRitenuta 92.0 but created invoice has got "
            "144.0\n."
        )

    def test_41_xml_import_withholding(self):
        res = self.run_wizard('test41', 'IT01234567890_FPR12.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 2)
        self.assertAlmostEquals(invoice.amount_total, 1220.0)
        self.assertAlmostEquals(invoice.withholding_tax_amount, 94.0)
        self.assertAlmostEquals(invoice.amount_net_pay, 1126.0)

    def test_42_xml_import_withholding(self):
        # cassa previdenziale sulla quale è applicata la ritenuta
        res = self.run_wizard('test42', 'IT01234567890_FPR13.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_total, 19032.0)
        self.assertEqual(invoice.withholding_tax_amount, 3120.0)
        self.assertEqual(invoice.amount_net_pay, 15912.0)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 1)
        self.assertTrue(len(invoice.invoice_line_ids) == 2)

    def test_43_xml_import_withholding(self):
        # Avvocato Mario Bianchi di Ferrara.
        # Imponibile di 100+15% spese
        res = self.run_wizard('test43', 'ITBNCMRA80A01D548T_20001.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.withholding_tax_amount, 23.0)
        self.assertTrue(len(invoice.ftpa_withholding_ids), 1)
        self.assertTrue(len(invoice.invoice_line_ids) == 3)

    def test_44_xml_import(self):
        res = self.run_wizard('test44', 'ITBNCMRA80A01D548T_20005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.invoice_line_ids) == 3)

    def test_45_xml_import_no_duplicate_partner(self):
        partner_id = self.env['res.partner'].search([
            ('vat', 'ilike', '05979361218')
        ])
        partner_id.vat = ' %s  ' % partner_id.vat
        res = self.run_wizard('test45', 'IT05979361218_001.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.id, partner_id.id)
        self.assertEqual(
            len(self.env['res.partner'].search([
                ('vat', 'ilike', '05979361218')
            ])), 1)

    def test_46_xml_import(self):
        wiz_values = {'e_invoice_detail_level': '0'}
        res = self.run_wizard('test46', 'IT05979361218_016.xml', wiz_values=wiz_values)
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEqual(invoice.e_invoice_amount_untaxed, 34.32)
        self.assertEqual(invoice.e_invoice_amount_tax, 0.0)
        self.assertEqual(invoice.e_invoice_amount_total, 34.32)

    def test_47_xml_import(self):
        res = self.run_wizard('test47', 'IT01234567890_FPR14.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(invoice.e_invoice_validation_error)
        self.assertTrue(
            "Untaxed amount (44480.0) does not match with e-bill untaxed amount "
            "(44519.26)" in invoice.e_invoice_validation_message)
        # Due to multiple SQL transactions, we cannot test the correct importation.
        # IT01234567890_FPR14.xml should be tested manually

    def test_48_xml_import(self):
        # bank account already exists for another partner
        # invoice creation must not be blocked
        to_unlink = []
        bank = self.env["res.bank"].create({
            "bic": "BCITITMM",
            "name": "Other Bank",
        })
        to_unlink.append(bank)
        partner = self.env["res.partner"].create({
            "name": "Some Other Company",
        })
        to_unlink.append(partner)
        self.env["res.partner.bank"].create({
            "acc_number": "IT59R0100003228000000000622",
            "company_id": self.env.user.company_id.id,
            "partner_id": partner.id,
        })
        res = self.run_wizard('test48', 'IT01234567890_FPR15.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(
            "Bank account IT59R0100003228000000000622 already exists" in
            invoice.inconsistencies)
        for model in to_unlink:
            model.unlink()

    def test_49_xml_import(self):
        res = self.run_wizard('test49', 'IT01234567890_FPR16.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.carrier_id.vat, "IT04102770965")

    def test_50_xml_import(self):
        # this method name is used in 14.0
        # reserving to make porting easier
        pass

    def test_51_xml_import(self):
        res = self.run_wizard("test51", "IT02780790107_11008.xml")
        invoice_ids = res.get("domain")[0][2]
        invoice = self.invoice_model.browse(invoice_ids)
        self.assertTrue(invoice.fatturapa_attachment_in_id.is_self_invoice)

    def test_52_xml_import(self):
        """
        Check that an XML with syntax error is created,
        but it shows a parsing error.
        """
        attachment = self.create_attachment(
            "test52",
            "ZGEXQROO37831_anonimizzata.xml",
        )
        self.assertIn('syntax error',
                      attachment.e_invoice_parsing_error)

    def test_53_xml_import(self):
        """
        Check that VAT of non-IT partner is not checked.
        """
        partner_model = self.env['res.partner']
        # Arrange: A partner with vat GB99999999999 does not exist
        not_valid_vat = 'GB99999999999'

        def vat_partner_exists():
            return partner_model.search([
                ('vat', '=', not_valid_vat),
            ])
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
            partner_model.create([{
                'name': "Test not valid VAT",
                'country_id': self.ref('base.uk'),
                'vat': not_valid_vat,
            }])
        exc_message = ve.exception.args[0]
        self.assertRegex(
            exc_message,
            'VAT number .*{not_valid_vat}.* does not seem to be valid'
            .format(
                not_valid_vat=not_valid_vat,
            )
        )

    def _check_invoice_configured_date(self, invoice, configured_date):
        """
        Check that `invoice`'s Accounting Date is `configured date`.
        Also check that resetting to draft and validating again
        does not change the `invoice`'s Accounting Date.
        """
        self.assertEqual(
            invoice.date,
            configured_date,
            "Configured date not set in the invoice after import",
        )

        invoice.action_invoice_cancel()
        invoice.action_invoice_draft()
        invoice.action_invoice_open()

        self.assertEqual(
            invoice.date,
            configured_date,
            "Configured date not set in the invoice after reset to draft",
        )

    def test_xml_import_rec_date(self):
        """
        Set 'Vendor invoice registration default date' to 'Received Date'.

        Check that the received date is set during the import
        and kept after reset to draft and validation.
        """
        company = self.env.user.company_id
        company.in_invoice_registration_date = 'rec_date'

        res = self.run_wizard('xml_import_rec_date', 'IT05979361218_013.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        self._check_invoice_configured_date(
            invoice,
            invoice.e_invoice_received_date,
        )

        # Update the reference so that importing the same file
        # (in other tests) does not raise "Duplicated vendor reference..."
        invoice.reference = 'xml_import_rec_date'

    def test_xml_import_inv_date(self):
        """
        Set 'Vendor invoice registration default date' to 'Invoice Date'.

        Check that the invoice date is set during the import
        and kept after reset to draft and validation.
        """
        company = self.env.user.company_id
        company.in_invoice_registration_date = 'inv_date'

        res = self.run_wizard('xml_import_inv_date', 'IT05979361218_013.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)

        self._check_invoice_configured_date(
            invoice,
            invoice.date_invoice,
        )

        # Update the reference so that importing the same file
        # (in other tests) does not raise "Duplicated vendor reference..."
        invoice.reference = 'xml_import_inv_date'

    def test_54_xml_import(self):
        # Payments may refer to our own bank account (SEPA)
        to_unlink = []
        bank = self.env["res.bank"].create({
            "bic": "BCITITMM",
            "name": "Other Bank",
        })
        to_unlink.append(bank)
        bank_account = self.env["res.partner.bank"].create({
            "acc_number": "IT59R0100003228000000000622",
            "company_id": self.env.user.company_id.id,
            "partner_id": self.env.user.company_id.partner_id.id,
        })
        to_unlink.append(bank_account)
        res = self.run_wizard('test54', 'IT01234567890_FPR15.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertIn(
            invoice.fatturapa_payments[0].payment_methods[0].payment_bank_iban,
            invoice.company_id.partner_id.bank_ids.mapped("acc_number")
        )
        self.assertFalse(
            "Bank account IT59R0100003228000000000622 already exists" in
            invoice.inconsistencies)
        for model in to_unlink:
            model.unlink()

    def test_55_duplicated_partner(self):
        """If there are multiple partners with the same VAT
        and we try to import an Electronic Invoice for that VAT,
        an exception is raised."""
        # Arrange: There are two partners with the same VAT
        common_vat = 'IT03309970733'
        partners = self.env['res.partner'].create([
            {
                'name': "Test partner1",
                'vat': common_vat,
            },
            {
                'name': "Test partner2",
                'vat': common_vat,
            },
        ])

        # Update any conflicting partner from other tests
        existing_partners = self.env['res.partner'].search(
            [
                ('sanitized_vat', '=', common_vat),
                ('id', 'not in', partners.ids),
            ],
        )
        existing_partners.update({
            'vat': 'IT12345670017',
        })

        # Assert: The import wizard can't choose between the two created partners
        with self.assertRaises(UserError) as ue:
            self.run_wizard('VATG1', 'IT03309970733_VATG1.xml')
        exc_message = ue.exception.args[0]
        self.assertIn("Two distinct partners", exc_message)
        self.assertIn("VAT number", exc_message)
        for partner in partners:
            self.assertIn(partner.name, exc_message)

    def test_56_xml_import_vat_group(self):
        """Importing bills from VAT groups creates different suppliers."""
        # Arrange: The involved XMLs contain suppliers from a VAT group:
        # the suppliers have the same VAT `common_vat`,
        # but each supplier has a different fiscal code
        common_vat = 'IT03309970733'
        vat_group_1_fiscalcode = 'MRORSS90E25B111T'
        vat_group_2_fiscalcode = '03533590174'

        # Update any conflicting partner from other tests
        existing_partners = self.env['res.partner'].search(
            [
                '|',
                ('sanitized_vat', '=', common_vat),
                ('fiscalcode', 'in', (
                    vat_group_1_fiscalcode,
                    vat_group_2_fiscalcode,
                )),
            ],
        )
        existing_partners.update({
            'vat': 'IT12345670017',
            'fiscalcode': '1234567890123456',
        })

        # Act: Import the XMLs,
        # checking that the suppliers match the data in the XML
        res = self.run_wizard('VATG1', 'IT03309970733_VATG1.xml')
        invoice_model = res.get('res_model')
        invoice_domain = res.get('domain')
        invoice_vat_group_1 = self.env[invoice_model].search(invoice_domain)
        vat_group_1_partner = invoice_vat_group_1.partner_id
        self.assertEqual(vat_group_1_partner.sanitized_vat, common_vat)
        self.assertEqual(vat_group_1_partner.fiscalcode, vat_group_1_fiscalcode)

        res = self.run_wizard('VATG2', 'IT03309970733_VATG2.xml')
        invoice_model = res.get('res_model')
        invoice_domain = res.get('domain')
        invoice_vat_group_2 = self.env[invoice_model].search(invoice_domain)
        vat_group_2_partner = invoice_vat_group_2.partner_id
        self.assertEqual(vat_group_2_partner.sanitized_vat, common_vat)
        self.assertEqual(vat_group_2_partner.fiscalcode, vat_group_2_fiscalcode)

        # Assert: Two different partners have been created
        self.assertNotEqual(
            vat_group_1_partner,
            vat_group_2_partner,
        )

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

    def test_01_xml_zero_quantity_line(self):
        res = self.run_wizard('test_zeroq_01', 'IT05979361218_q0.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 0)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1)

    def test_xml_import_summary_tax_rate(self):
        # Invoice  with positive total. Detail Level:  '1' -- Tax Rate
        supplier = self.env['res.partner'].search(
            [('vat', '=', 'IT02780790107')])[0]
        # in order to make the system create the invoice lines
        supplier.e_invoice_detail_level = '1'
        res = self.run_wizard('test_summary_tax_rate',
                              'IT05979361218_ripilogoiva.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_total, 204.16)
        self.assertEqual(len(invoice.invoice_line_ids), 2)

        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 164.46)
        self.assertEqual(invoice.invoice_line_ids[0].quantity, 1.0)
        self.assertEqual(invoice.invoice_line_ids[1].price_unit, 3.52)
        self.assertEqual(invoice.invoice_line_ids[1].quantity, 1.0)


class TestFatturaPAEnasarco(FatturapaCommon):

    def setUp(self):
        super(TestFatturaPAEnasarco, self).setUp()

        self.invoice_model = self.env['account.invoice']

    def test_01_xml_import_enasarco(self):
        account_payable = self.env['account.account'].create({
            'name': 'Test WH tax',
            'code': 'whtaxpay2',
            'user_type_id': self.env.ref(
                'account.data_account_type_payable').id,
            'reconcile': True})
        account_receivable = self.env['account.account'].create({
            'name': 'Test WH tax',
            'code': 'whtaxrec2',
            'user_type_id': self.env.ref(
                'account.data_account_type_receivable').id,
            'reconcile': True})
        misc_journal = self.env['account.journal']. \
            search([("code", "=", "MISC")])
        self.env['withholding.tax'].create({
            'name': 'Enasarco',
            'code': 'TC07',
            'account_receivable_id': account_receivable.id,
            'account_payable_id': account_payable.id,
            'journal_id': misc_journal.id,
            'payment_term': self.env.ref(
                'account.account_payment_term_advance').id,
            'wt_types': 'enasarco',
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.r').id,
            'rate_ids': [(0, 0, {
                'tax': 1.57,
                'base': 1.0,
            })]
        })
        self.env['withholding.tax'].create({
            'name': 'Enasarco 8,50',
            'code': 'TC07',
            'account_receivable_id': account_receivable.id,
            'account_payable_id': account_payable.id,
            'journal_id': misc_journal.id,
            'payment_term': self.env.ref(
                'account.account_payment_term_advance').id,
            'wt_types': 'enasarco',
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.r').id,
            'rate_ids': [(0, 0, {
                'tax': 8.5,
                'base': 1.0,
            })]
        })
        self.env['withholding.tax'].create({
            'name': '1040/3',
            'code': '1040',
            'account_receivable_id': account_receivable.id,
            'account_payable_id': account_payable.id,
            'journal_id': misc_journal.id,
            'payment_term': self.env.ref(
                'account.account_payment_term_advance').id,
            'wt_types': 'ritenuta',
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.a').id,
            'rate_ids': [(0, 0, {
                'tax': 11.50,
                'base': 1.0,
            })]
        })
        self.env['withholding.tax'].create({
            'name': '1040 R',
            'code': '1040R',
            'account_receivable_id': account_receivable.id,
            'account_payable_id': account_payable.id,
            'journal_id': misc_journal.id,
            'payment_term': self.env.ref(
                'account.account_payment_term_advance').id,
            'wt_types': 'ritenuta',
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.r').id,
            'rate_ids': [(0, 0, {
                'tax': 11.50,
                'base': 1.0,
            })]
        })
        # case with ENASARCO only in DatiCassaPrevidenziale and not in DatiRitenuta.
        # This should not happen, but it is valid for SDI
        res = self.run_wizard('test01', 'IT05979361218_014.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.amount_untaxed, 2470.00)
        self.assertEqual(invoice.amount_tax, 543.40)
        self.assertEqual(invoice.amount_total, 3013.40)
        self.assertEqual(invoice.amount_net_pay, 2729.35)
        self.assertEqual(invoice.withholding_tax_amount, 284.05)
        self.assertEqual(invoice.welfare_fund_ids[0].kind_id.code, 'N2.2')
        self.assertTrue(len(invoice.e_invoice_line_ids) == 1)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].name, 'ACCONTO PROVVIGIONI')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].qty, 1.0)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].unit_price, 2470.0)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].total_price, 2470.0)

    def test_02_xml_import_enasarco(self):
        # Giacomo Neri, agente di commercio di Firenze.
        # Imponibile 10
        res = self.run_wizard('test02', 'ITNREGCM80H30D612D_20003.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.amount_untaxed, 10.0)
        self.assertEqual(invoice.amount_tax, 2.2)
        self.assertEqual(invoice.amount_total, 12.2)
        self.assertEqual(invoice.amount_net_pay, 10.2)
        self.assertTrue(len(invoice.invoice_line_ids) == 1)

    def test_03_xml_import_enasarco(self):
        # Come sopra, ma senza "<Ritenuta>SI</Ritenuta>" in riga fattura
        res = self.run_wizard('test03', 'ITNREGCM80H30D612D_20004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(
            'E-bill contains DatiRitenuta but no lines subjected to Ritenuta was found'
            in invoice.e_invoice_validation_message)
        self.assertEqual(invoice.amount_total, 12.2)
        self.assertEqual(invoice.amount_net_pay, 12.2)
