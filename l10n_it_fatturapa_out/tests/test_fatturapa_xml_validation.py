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
from openerp import workflow
import openerp.tests.common as test_common
from openerp.modules.module import get_module_resource


class TestFatturaPAXMLValidation(test_common.SingleTransactionCase):

    def getFile(self, filename):
        path = get_module_resource('l10n_it_fatturapa_out',
                                   'tests', 'data', filename)
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
        self.wizard_model = self.registry('wizard.export.fatturapa')
        self.data_model = self.registry('ir.model.data')
        self.attach_model = self.registry('fatturapa.attachment.out')

    def set_sequences(self, file_number, invoice_number):
        cr, uid = self.cr, self.uid
        seq_pool = self.registry('ir.sequence')
        seq_id = self.data_model.get_object_reference(
            cr, uid, 'l10n_it_fatturapa', 'seq_fatturapa')
        seq_pool.write(cr, uid, [seq_id[1]], {
            'implementation': 'no_gap',
            'number_next_actual': file_number,
            })
        seq_id = self.data_model.get_object_reference(
            cr, uid, 'account', 'sequence_sale_journal')
        seq_pool.write(cr, uid, [seq_id[1]], {
            'implementation': 'no_gap',
            'number_next_actual': invoice_number,
            })

    def confirm_invoice(self, invoice_xml_id):
        cr, uid = self.cr, self.uid

        invoice_id = self.data_model.get_object_reference(
            cr, uid, 'l10n_it_fatturapa', invoice_xml_id)
        if invoice_id:
            invoice_id = invoice_id and invoice_id[1] or False

        workflow.trg_validate(
            uid, 'account.invoice', invoice_id, 'invoice_open', cr)
        return invoice_id

    def run_wizard(self, invoice_id):
        cr, uid = self.cr, self.uid
        wizard_id = self.wizard_model.create(cr, uid, {})
        return self.wizard_model.exportFatturaPA(
            cr, uid, wizard_id, context={'active_ids': [invoice_id]})

    def check_content(self, xml_content, file_name):
        test_fatt_data = self.getFile(file_name)[1]
        test_fatt_content = test_fatt_data.decode('base64').decode('latin1')
        self.assertEqual(
            test_fatt_content.replace('\n', ''), xml_content.replace('\n', ''))

    def test_0_xml_export(self):
        cr, uid = self.cr, self.uid
        self.set_sequences(1, 13)
        invoice_id = self.confirm_invoice('fatturapa_invoice_0')
        res = self.run_wizard(invoice_id)

        self.assertTrue(res, 'Export failed.')
        attachment = self.attach_model.browse(cr, uid, res['res_id'])
        self.assertEqual(attachment.datas_fname, 'IT06363391001_00001.xml')

        # XML doc to be validated
        xml_content = attachment.datas.decode('base64').decode('latin1')
        self.check_content(xml_content, 'IT06363391001_00001.xml')

    def test_1_xml_export(self):
        cr, uid = self.cr, self.uid
        self.set_sequences(2, 14)
        invoice_id = self.confirm_invoice('fatturapa_invoice_1')
        res = self.run_wizard(invoice_id)
        attachment = self.attach_model.browse(cr, uid, res['res_id'])

        xml_content = attachment.datas.decode('base64').decode('latin1')
        self.check_content(xml_content, 'IT06363391001_00002.xml')
