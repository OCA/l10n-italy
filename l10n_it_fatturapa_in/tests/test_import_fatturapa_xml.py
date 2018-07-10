# -*- coding: utf-8 -*-

import base64
import tempfile
from odoo.tests.common import SingleTransactionCase
from odoo.modules import get_module_resource
from odoo.exceptions import UserError


class TestFatturaPAXMLValidation(SingleTransactionCase):

    def getFile(self, filename):
        path = get_module_resource(
            'l10n_it_fatturapa_in', 'tests', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def create_wt(self):
        return self.env['withholding.tax'].create({
            'name': '1040',
            'code': '1040',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'rate_ids': [(0, 0, {'tax': 20.0})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.a').id,
        })

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.wizard_model = self.env['wizard.import.fatturapa']
        self.data_model = self.env['ir.model.data']
        self.attach_model = self.env['fatturapa.attachment.in']
        self.invoice_model = self.env['account.invoice']
        self.payable_account_id = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)
        ], limit=1).id

    def run_wizard(self, name, file_name):
        attach_id = self.attach_model.create(
            {
                'name': name,
                'datas': self.getFile(file_name)[1],
                'datas_fname': file_name
            }).id
        wizard = self.wizard_model.create({})
        return wizard.with_context(active_ids=[attach_id]).importFatturaPA()

    def run_wizard_multi(self, file_name_list):
        active_ids = []
        for file_name in file_name_list:
            active_ids.append(self.attach_model.create(
                {
                    'name': file_name,
                    'datas': self.getFile(file_name)[1],
                    'datas_fname': file_name
                }).id)
        wizard = self.wizard_model.create({})
        return wizard.with_context(active_ids=active_ids).importFatturaPA()

    def test_00_xml_import(self):
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
            '22% ftPA acq')
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_untaxed, 34.00)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_tax, 7.48)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].payability, 'D')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(invoice.partner_id.state_id.code, "SS")
        self.assertEqual(
            invoice.tax_representative_id.name, "Rappresentante fiscale")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_rate_tax, 0.04)
        self.assertEqual(
            invoice.related_documents[0].type, "order")
        self.assertEqual(
            invoice.related_documents[0].cig, '456def')
        self.assertEqual(
            invoice.related_documents[0].cup, '123abc')
        self.assertEqual(
            invoice.welfare_fund_ids[0].welfare_amount_tax, 9)
        self.assertFalse(invoice.welfare_fund_ids[0].welfare_taxable)
        self.assertEqual(invoice.unit_weight, 'KGM')
        self.assertEqual(invoice.ftpa_incoterms, 'DAP')
        self.assertEqual(invoice.fiscal_document_type_id.code, 'TD01')
        self.assertTrue(invoice.art73)

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

    # def test_03_xml_import(self):
    #     res = self.run_wizard('test3', 'IT05979361218_002.xml.p7m')
    #     invoice_id = res.get('domain')[0][2][0]
    #     invoice = self.invoice_model.browse(invoice_id)
    #     self.assertEqual(invoice.partner_id.register_code, 'TO1258B')
    #     self.assertEqual(
    #         invoice.partner_id.register_fiscalpos.code, 'RF02')
    #     self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0007')
    #     self.assertEqual(invoice.amount_total, 54.00)

    def test_04_xml_import(self):
        res = self.run_wizard('test4', 'IT02780790107_11005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, '124')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].name,
            '22% ftPA acq')
        self.assertEqual(
            invoice.invoice_line_ids[1].invoice_line_tax_ids[0].name,
            '22% ftPA acq')
        self.assertEqual(
            invoice.invoice_line_ids[0].invoice_line_tax_ids[0].amount, 22)
        self.assertEqual(
            invoice.invoice_line_ids[1].invoice_line_tax_ids[0].amount, 22)
        self.assertEqual(
            invoice.invoice_line_ids[1].price_unit, 2)
        self.assertEqual(
            invoice.invoice_line_ids[0].cod_article_ids[0].name, 'EAN')
        self.assertEqual(
            invoice.invoice_line_ids[0].cod_article_ids[0].code_val, '12345')
        self.assertEqual(
            invoice.inconsistencies,
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"')

    def test_05_xml_import(self):
        res = self.run_wizard('test5', 'IT05979361218_003.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0008')
        self.assertEqual(invoice.sender, 'TZ')
        self.assertEqual(invoice.intermediary.name, 'ROSSI MARIO')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')
        self.assertEqual(
            invoice.invoice_line_ids[0].discount_rise_price_ids[0].name, 'SC')
        self.assertEqual(
            invoice.invoice_line_ids[0].discount_rise_price_ids[0].percentage,
            10)
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
            ' DatiRiepilogo 1173.6')

    def test_10_xml_import(self):
        # Fix Date format
        res = self.run_wizard('test6', 'IT05979361218_007.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0009')
        self.assertEqual(
            invoice.date_invoice, '2015-03-16')
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_due_date,
            '2015-06-03'
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
        self.assertEqual(invoice.intermediary.name, 'ROSSI MARIO')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')

    def test_13_xml_import(self):
        # inconsistencies must not be duplicated
        res = self.run_wizard_multi([
            'IT02780790107_11005.xml',
            'IT02780790107_11005.xml',
            ])
        invoice1_id = res.get('domain')[0][2][0]
        invoice2_id = res.get('domain')[0][2][1]
        invoice1 = self.invoice_model.browse(invoice1_id)
        invoice2 = self.invoice_model.browse(invoice2_id)
        self.assertEqual(
            invoice1.inconsistencies,
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"')
        self.assertEqual(
            invoice2.inconsistencies,
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"')

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
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"\n'
            u'XML contains tax with percentage "15.55"'
            ' but it does not exist in your system\n'
            'XML contains tax with percentage "15.55"'
            ' but it does not exist in your system')

    def test_15_xml_import(self):
        self.wt = self.create_wt()
        res = self.run_wizard('test15', 'IT05979361218_009.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertAlmostEquals(invoice.withholding_tax_amount, 1)
        self.assertAlmostEquals(invoice.amount_total, 6.1)
        self.assertAlmostEquals(invoice.amount_net_pay, 5.1)
