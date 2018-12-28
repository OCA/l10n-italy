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

    def test_05_xml_import(self):
        self.env.user.company_id.dati_bollo_product_id = (
            self.service.id)
        res = self.run_wizard('test5', 'IT05979361218_003.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.reference, 'FT/2015/0008')
        self.assertEqual(invoice.sender, 'TZ')
        self.assertEqual(invoice.intermediary.name, 'ROSSI MARIO')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')
        bollo_found = False
        for line in invoice.invoice_line:
            if line.product_id.id == self.service.id:
                self.assertEqual(line.price_unit, 6)
                bollo_found = True
        self.assertTrue(bollo_found)
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].name,
            'SC')
        self.assertEqual(
            invoice.e_invoice_line_ids[0].discount_rise_price_ids[0].
            percentage, 10
        )
        self.assertEqual(invoice.amount_untaxed, 15)
        self.assertEqual(invoice.amount_tax, 0)
        self.assertEqual(invoice.amount_total, 15)

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
        self.assertEqual(invoice.invoice_line[0].admin_ref, 'D122353')


