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
import netsvc
import openerp.tests.common as test_common
from openerp import addons
from datetime import datetime
from lxml import etree
import shutil
import os


class TestFatturaPAXMLValidation(test_common.SingleTransactionCase):

    def getFilePath(self, filepath):
        with open(filepath) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return filepath, out.read()

    def getAttacment(self, name):
        path = addons.get_module_resource(
            'l10n_it_fatturapa_out',
            'tests', 'data', 'attah_base.pdf'
        )
        currDir = os.path.dirname(path)
        new_file = '%s/%s' % (currDir, name)
        shutil.copyfile(path, new_file)
        return self.getFilePath(new_file)

    def getFile(self, filename):
        path = addons.get_module_resource(
            'l10n_it_fatturapa_out', 'tests', 'data', filename)
        return self.getFilePath(path)

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        cr, uid = self.cr, self.uid
        self.wizard_model = self.registry('wizard.export.fatturapa')
        self.data_model = self.registry('ir.model.data')
        self.attach_model = self.registry('fatturapa.attachment.out')
        self.invoice_model = self.registry('account.invoice')
        self.fatturapa_attach = self.registry('fatturapa.attachments')
        self.company_model = self.registry('res.company')
        self.context = {}
        self.maxDiff = None
        company_id = self.data_model.get_object_reference(
            cr, uid, 'base', 'main_company')[1]
        account_ova_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'ova')[1]
        self.company = self.company_model.browse(cr, uid, company_id)
        self.company.write({'sp_account_id': account_ova_id})

    def attachFileToInvoice(self, InvoiceId, filename):
        self.fatturapa_attach.create(
            self.cr, self.uid,
            {
                'name': filename,
                'invoice_id': InvoiceId,
                'datas': self.getAttacment(filename)[1],
                'datas_fname': filename
            }
        )

    def checkCreateFiscalYear(self, date_to_check):
        '''
        with this method you can check if a date
        passed in param dae_to_check , is in
        current fiscal year .
        If not present, it creates a fiscal year and
        a sequence for sale_journal,
        consistent with date, in date_to_check.
        '''
        cr, uid = self.cr, self.uid
        self.fy_model = self.registry('account.fiscalyear')
        if not self.fy_model.find(
            cr, uid, dt=date_to_check, exception=False
        ):
            ds = datetime.strptime(date_to_check, '%Y-%m-%d')
            seq_id = self.data_model.get_object_reference(
                cr, uid, 'account', 'sequence_sale_journal')
            year = ds.date().year
            name = '%s' % year
            code = 'FY%s' % year
            start = '%s-01-01' % year
            stop = '%s-12-31' % year
            fy_id = self.fy_model.create(
                cr, uid,
                {
                    'name': name,
                    'code': code,
                    'date_start': start,
                    'date_stop': stop
                }
            )
            self.fy_model.create_period(cr, uid, [fy_id])
            self.fiscalyear_id = fy_id
            seq_name = 'seq%s' % name
            self.context['fiscalyear_id'] = self.fiscalyear_id
            prefix = 'SAJ/%s/' % year
            s_id = self.registry('ir.sequence').create(
                cr, uid,
                {
                    'name': seq_name,
                    'padding': 3,
                    'prefix': prefix
                }
            )
            self.context['sequence_id'] = s_id
            self.registry('account.sequence.fiscalyear').create(
                cr, uid,
                {
                    "sequence_id": s_id,
                    'sequence_main_id': seq_id[1],
                    "fiscalyear_id": self.fiscalyear_id
                },
                context=self.context
            )

    def set_sequences(self, file_number, invoice_number):
        cr, uid = self.cr, self.uid
        seq_pool = self.registry('ir.sequence')
        seq_id = self.data_model.get_object_reference(
            cr, uid, 'l10n_it_fatturapa', 'seq_fatturapa')
        seq_pool.write(cr, uid, [seq_id[1]], {
            'implementation': 'no_gap',
            'number_next_actual': file_number,
            }
        )
        if self.context.get('fiscalyear_id'):
            seq_id = (0, self.context.get('sequence_id'))
        else:
            seq_id = self.data_model.get_object_reference(
                cr, uid, 'account', 'sequence_sale_journal')
        seq_pool.write(
            cr, uid, [seq_id[1]],
            {
                'implementation': 'no_gap',
                'number_next_actual': invoice_number,
            },
            context=self.context
        )

    def confirm_invoice(self, invoice_xml_id, attach=False):
        cr, uid = self.cr, self.uid

        invoice_id = self.data_model.get_object_reference(
            cr, uid, 'l10n_it_fatturapa', invoice_xml_id)
        if invoice_id:
            invoice_id = invoice_id and invoice_id[1] or False
        # this  write updates context with
        # fiscalyear_id
        if attach:
            self.attachFileToInvoice(invoice_id, 'test1.pdf')
            self.attachFileToInvoice(invoice_id, 'test2.pdf')
        self.invoice_model.write(
            cr, uid, invoice_id, {}, context=self.context)
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(
            uid, 'account.invoice', invoice_id, 'invoice_open', cr
        )
        return invoice_id

    def run_wizard(self, invoice_id):
        cr, uid = self.cr, self.uid
        wizard_id = self.wizard_model.create(cr, uid, {})
        return self.wizard_model.exportFatturaPA(
            cr, uid, wizard_id, context={'active_ids': [invoice_id]})

    def check_content(self, xml_content, file_name):
        parser = etree.XMLParser(remove_blank_text=True)
        test_fatt_data = self.getFile(file_name)[1]
        test_fatt_content = test_fatt_data.decode('base64')
        test_fatt = etree.fromstring(test_fatt_content, parser)
        xml = etree.fromstring(xml_content, parser)
        self.assertEqual(etree.tostring(test_fatt), etree.tostring(xml))

    def test_0_xml_export(self):
        cr, uid = self.cr, self.uid
        self.checkCreateFiscalYear('2014-01-07')
        self.context['fiscalyear_id'] = self.fiscalyear_id
        self.set_sequences(1, 13)
        invoice_id = self.confirm_invoice('fatturapa_invoice_0')
        res = self.run_wizard(invoice_id)

        self.assertTrue(res, 'Export failed.')
        attachment = self.attach_model.browse(cr, uid, res['res_id'])
        self.assertEqual(attachment.datas_fname, 'IT06363391001_00001.xml')

        # XML doc to be validated
        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00001.xml')

    def test_1_xml_export(self):
        cr, uid = self.cr, self.uid
        self.checkCreateFiscalYear('2015-06-15')
        self.set_sequences(2, 14)
        invoice_id = self.confirm_invoice('fatturapa_invoice_1')
        res = self.run_wizard(invoice_id)
        attachment = self.attach_model.browse(cr, uid, res['res_id'])

        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00002.xml')

    def test_2_xml_export(self):
        cr, uid = self.cr, self.uid
        self.checkCreateFiscalYear('2015-06-15')
        self.set_sequences(3, 15)
        invoice_id = self.confirm_invoice('fatturapa_invoice_2', attach=True)
        res = self.run_wizard(invoice_id)
        attachment = self.attach_model.browse(cr, uid, res['res_id'])
        xml_content = attachment.datas.decode('base64')

        self.check_content(xml_content, 'IT06363391001_00003.xml')

    def test_3_xml_export(self):
        cr, uid = self.cr, self.uid
        self.checkCreateFiscalYear('2015-06-15')
        self.set_sequences(4, 16)
        invoice_id = self.confirm_invoice('fatturapa_invoice_3')
        res = self.run_wizard(invoice_id)
        attachment = self.attach_model.browse(cr, uid, res['res_id'])
        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00004.xml')

    def test_9_xml_export(self):
        self.tax_22.price_include = True
        self.set_sequences(9, 18, '2018-01-07')
        partner = self.res_partner_fatturapa_4
        partner.onchange_country_id_e_inv()
        partner.write(partner._convert_to_write(partner._cache))
        self.assertEqual(partner.codice_destinatario, 'XXXXXXX')
        invoice = self.invoice_model.create({
            'date_invoice': '2018-01-07',
            'partner_id': partner.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.AED.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_id': [(6, 0, {
                        self.tax_22.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+ Antivirus',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_id': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.assertEqual(attachment.datas_fname, 'IT06363391001_00009.xml')

        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00009.xml')