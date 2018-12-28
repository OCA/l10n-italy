# -*- coding: utf-8 -*-

import base64
import tempfile
from openerp.tests.common import SingleTransactionCase
from openerp.modules import get_module_resource
from openerp.exceptions import Warning as UserError


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
            ('user_type', '=', self.env.ref(
                'account.data_account_type_payable').id)
        ], limit=1).id
        self.headphones = self.env.ref(
            'product.product_product_7_product_template')
        self.imac = self.env.ref(
            'product.product_product_8_product_template')
        self.service = self.env.ref('product.product_product_consultant')
        self.state = self.env['res.country.state']
        self.state.create({
            'code': 'SS',
            'name': 'Sassari',
            'country_id': self.env['res.country'].search(
                [('code', '=', 'IT')]).id
        })

    def run_wizard(self, name, file_name):
        attach_id = self.attach_model.create(
            {
                'name': name,
                'datas': self.getFile(file_name)[1],
                'datas_fname': file_name
            }).id
        wizard = self.wizard_model.with_context(
            active_ids=[attach_id]).create({})
        return wizard.importFatturaPA()

    def run_wizard_multi(self, file_name_list):
        active_ids = []
        for file_name in file_name_list:
            active_ids.append(self.attach_model.create(
                {
                    'name': file_name,
                    'datas': self.getFile(file_name)[1],
                    'datas_fname': file_name
                }).id)
        wizard = self.wizard_model.with_context(
            active_ids=active_ids).create({})
        return wizard.importFatturaPA()

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
        for line in invoice.invoice_line:
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
            len(invoice.invoice_line[0].invoice_line_tax_id), 1)
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].name,
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

    def test_04_xml_import(self):
        res = self.run_wizard('test4', 'IT02780790107_11005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, '124')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].name,
            '22% ftPA acq')
        self.assertEqual(
            invoice.invoice_line[1].invoice_line_tax_id[0].name,
            '22% ftPA acq')
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].amount, 0.22)
        self.assertEqual(
            invoice.invoice_line[1].invoice_line_tax_id[0].amount, 0.22)
        self.assertEqual(
            invoice.invoice_line[1].price_unit, 2)
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
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"\n\n')

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
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"\n\n')
        self.assertEqual(
            invoice2.inconsistencies,
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"\n\n')

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
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"\n\n'
            u'XML contains tax with percentage "15.55"'
            ' but it does not exist in your system\n'
            'XML contains tax with percentage "15.55"'
            ' but it does not exist in your system')

    def test_16_xml_import(self):
        # file B2B downloaded from
        # http://www.fatturapa.gov.it/export/fatturazione/it/a-3.htm
        res = self.run_wizard('test16', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertEqual(len(invoices), 2)
        for invoice in invoices:
            self.assertEqual(invoice.inconsistencies, '')
            self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertTrue(len(invoice.invoice_line) == 2)
                for line in invoice.invoice_line:
                    self.assertFalse(line.product_id)
            if invoice.reference == '456':
                self.assertTrue(len(invoice.invoice_line) == 1)
                for line in invoice.invoice_line:
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
        res = self.run_wizard('test17', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        for invoice in invoices:
            self.assertTrue(invoice.reference in ('456', '123'))
            if invoice.reference == '123':
                self.assertEqual(
                    invoice.invoice_line[0].product_id.id,
                    self.headphones.product_variant_ids[0].id
                )
            else:
                for line in invoice.invoice_line:
                    self.assertEqual(
                        line.product_id.id,
                        self.imac.product_variant_ids[0].id
                    )

        # change Livello di dettaglio Fatture elettroniche to Minimo
        partner.e_invoice_detail_level = '0'
        res = self.run_wizard('test17', 'IT01234567890_FPR03.xml')
        invoice_ids = res.get('domain')[0][2]
        invoices = self.invoice_model.browse(invoice_ids)
        self.assertTrue(len(invoices) == 2)
        for invoice in invoices:
            self.assertTrue(len(invoice.invoice_line) == 0)