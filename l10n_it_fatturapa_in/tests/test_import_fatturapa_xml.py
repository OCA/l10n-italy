# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
import tempfile
import openerp.tests.common as test_common
from openerp import addons
from openerp.osv.orm import except_orm


class TestFatturaPAXMLValidation(test_common.SingleTransactionCase):

    def getFile(self, filename):
        path = addons.get_module_resource('l10n_it_fatturapa_in',
                                          'tests', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.wizard_model = self.registry('wizard.import.fatturapa')
        self.data_model = self.registry('ir.model.data')
        self.attach_model = self.registry('fatturapa.attachment.in')
        self.invoice_model = self.registry('account.invoice')

    def run_wizard(self, name, file_name):
        cr, uid = self.cr, self.uid
        attach_id = self.attach_model .create(
            cr, uid,
            {
                'name': name,
                'datas': self.getFile(file_name)[1],
                'datas_fname': file_name
            })
        wizard_id = self.wizard_model.create(cr, uid, {})

        return self.wizard_model.importFatturaPA(
            cr, uid, wizard_id, context={'active_ids': [attach_id]})

    def test_0_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test0', 'IT05979361218_001.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.partner_id.register_code, 'TO1258B')
        self.assertEqual(
            invoice.partner_id.register_fiscalpos.code, 'RF02')
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0006')
        self.assertEqual(invoice.amount_total, 54.00)
        self.assertEqual(invoice.gross_weight, 0.00)
        self.assertEqual(invoice.net_weight, 0.00)

    def test_1_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test1', 'IT02780790107_11004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, '123')
        self.assertEqual(invoice.amount_untaxed, 25.00)
        self.assertEqual(invoice.amount_tax, 5.50)
        self.assertEqual(
            len(invoice.invoice_line[0].invoice_line_tax_id), 1)
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].name, '22%')
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_untaxed, 25.00)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_tax, 5.50)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].payability, 'D')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(invoice.partner_id.street, "VIALE ROMA 543")
        self.assertEqual(invoice.partner_id.province.code, "SS")
        self.assertEqual(
            invoice.tax_representative_id.name, "Rappresentante fiscale")
        self.assertEqual(invoice.welfare_fund_ids[0].welfare_rate_tax, 0.04)
        self.assertEqual(
            invoice.related_documents[0].type, "order")
        self.assertEqual(
            invoice.related_documents[0].cig, '456def')
        self.assertEqual(
            invoice.related_documents[0].cup, '123abc')

    def test_2_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test2', 'IT03638121008_X11111.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, '00001')
        self.assertEqual(invoice.amount_untaxed, 3)
        self.assertEqual(invoice.amount_tax, 0.66)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_untaxed, 3)
        self.assertEqual(
            invoice.fatturapa_summary_ids[0].amount_tax, 0.66)
        self.assertEqual(invoice.partner_id.name, "Societa' alpha S.r.l.")

    def test_3_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test3', 'IT05979361218_002.xml.p7m')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.partner_id.register_code, 'TO1258B')
        self.assertEqual(
            invoice.partner_id.register_fiscalpos.code, 'RF02')
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0007')
        self.assertEqual(invoice.amount_total, 54.00)

    def test_4_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test4', 'IT02780790107_11005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, '124')
        self.assertEqual(invoice.partner_id.name, "SOCIETA' ALPHA SRL")
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].name, '22%')
        self.assertEqual(
            invoice.invoice_line[1].invoice_line_tax_id[0].name, '22%')
        self.assertEqual(
            invoice.invoice_line[0].invoice_line_tax_id[0].amount, 0.22)
        self.assertEqual(
            invoice.invoice_line[1].invoice_line_tax_id[0].amount, 0.22)
        self.assertEqual(
            invoice.invoice_line[1].price_unit, 2)
        self.assertEqual(
            invoice.invoice_line[0].cod_article_ids[0].name, 'EAN')
        self.assertEqual(
            invoice.invoice_line[0].cod_article_ids[0].code_val, '12345')
        self.assertEqual(
            invoice.inconsistencies,
            u'DatiAnagrafici.Anagrafica.Denominazione contains "Societa\' '
            'Alpha SRL". Your System contains "SOCIETA\' ALPHA SRL"')

    def test_5_xml_import(self):
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test5', 'IT05979361218_003.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0008')
        self.assertEqual(invoice.sender, 'TZ')
        self.assertEqual(invoice.intermediary.name, 'ROSSI MARIO')
        self.assertEqual(invoice.intermediary.firstname, 'MARIO')
        self.assertEqual(invoice.intermediary.lastname, 'ROSSI')
        self.assertEqual(
            invoice.invoice_line[0].discount_rise_price_ids[0].name, 'SC')
        self.assertEqual(
            invoice.invoice_line[0].discount_rise_price_ids[0].percentage, 10)
        self.assertEqual(invoice.amount_untaxed, 9)
        self.assertEqual(invoice.amount_tax, 0)
        self.assertEqual(invoice.amount_total, 9)


    def test_6_import_except(self):
        # File not exist Exception
        self.assertRaises(
            Exception, self.run_wizard, 'test6_Exception', '')
        # fake Signed file is passed , generate orm_exception
        self.assertRaises(
            except_orm, self.run_wizard, 'test6_orm_exception',
            'IT05979361218_fake.xml.p7m'
        )

    def test_7_xml_import(self):
        cr, uid = self.cr, self.uid
        # 2 lines with quantity != 1 and discounts
        res = self.run_wizard('test7', 'IT05979361218_004.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0009')
        self.assertEqual(invoice.amount_untaxed, 1173.60)
        self.assertEqual(invoice.amount_tax, 258.19)
        self.assertEqual(invoice.amount_total, 1431.79)

    def test_8_xml_import(self):
        cr, uid = self.cr, self.uid
        # using ImportoTotaleDocumento
        res = self.run_wizard('test8', 'IT05979361218_005.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0010')
        self.assertEqual(invoice.amount_total, 1288.61)
        self.assertFalse(invoice.inconsistencies)

    def test_9_xml_import(self):
        cr, uid = self.cr, self.uid
        # using DatiGeneraliDocumento.ScontoMaggiorazione without
        # ImportoTotaleDocumento
        res = self.run_wizard('test9', 'IT05979361218_006.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0011')
        self.assertEqual(invoice.amount_total, 1288.61)
        self.assertEqual(
            invoice.inconsistencies,
            'Computed amount untaxed 1030.42 is different from'
            ' DatiRiepilogo 1173.6')

    def test_10_xml_import(self):
        # Fix Date format
        cr, uid = self.cr, self.uid
        res = self.run_wizard('test6', 'IT05979361218_007.xml')
        invoice_id = res.get('domain')[0][2][0]
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        self.assertEqual(invoice.supplier_invoice_number, 'FT/2015/0009')
        self.assertEqual(
            invoice.date_invoice, '2015-03-16')
        self.assertEqual(
            invoice.fatturapa_payments[0].payment_methods[0].payment_due_date,
            '2015-06-03'
        )
