# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Alessio Gerace <alessio.gerace@agilebg.com>
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


class TestFatturaPaInNotifications(test_common.SingleTransactionCase):

    def getFile(self, path):
        with open(path) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def getNotifFile(self, filename):
        path = addons.get_module_resource('l10n_it_fatturapa_in_notifications',
                                          'tests', 'data', filename)
        return self.getFile(path)

    def getFatturaFile(self, filename):
        path = addons.get_module_resource('l10n_it_fatturapa_in',
                                          'tests', 'data', filename)
        return self.getFile(path)

    def setUp(self):
        super(TestFatturaPaInNotifications, self).setUp()
        self.wizard_notif_model = self.registry(
            'wizard.fatturapa.import.notification')
        self.wizard_accept_model = self.registry(
            'wizard.fatturapa.in.accept')
        self.wizard_reject_model = self.registry(
            'wizard.fatturapa.in.reject')
        self.wizard_ftpa_model = self.registry('wizard.import.fatturapa')
        self.data_model = self.registry('ir.model.data')
        self.attach_model = self.registry('fatturapa.attachment.in')
        self.invoice_model = self.registry('account.invoice')
        self.notifications_model = self.registry('fatturapa.notification')

    def run_import_invoice_wizard(self, name, file_name):
        cr, uid = self.cr, self.uid
        attach_id = self.attach_model .create(
            cr, uid,
            {
                'name': name,
                'datas': self.getFatturaFile(file_name)[1],
                'datas_fname': file_name
            })
        wizard_id = self.wizard_ftpa_model.create(cr, uid, {})
        return self.wizard_ftpa_model.importFatturaPA(
            cr, uid, wizard_id, context={'active_ids': [attach_id]})

    def run_import_notif_wizard(self, file_name):
        cr, uid = self.cr, self.uid
        wizard_id = self.wizard_notif_model.create(
            cr, uid,
            {
                'name': self.getNotifFile(file_name)[1],
                'file_name': file_name,
                'invoice_type': 'supplier'
            }
        )
        return self.wizard_notif_model.import_file(
            cr, uid, [wizard_id], context={})

    def run_send_notif_wizard(self, message, invoice_id):
        cr, uid = self.cr, self.uid
        wizard_id = self.wizard_accept_model.create(
            cr, uid,
            {
                'name': message
            }
        )
        return self.wizard_accept_model.send(
            cr, uid, [wizard_id], context={'active_id': invoice_id})

    def run_send_rej_notif_wizard(self, message, invoice_id):
        cr, uid = self.cr, self.uid
        wizard_id = self.wizard_reject_model.create(
            cr, uid,
            {
                'name': message
            }
        )
        return self.wizard_reject_model.send(
            cr, uid, [wizard_id], context={'active_id': invoice_id})

    def check_content(self, xml_content, file_name):
        test_fatt_data = self.getNotifFile(file_name)[1]
        test_fatt_content = test_fatt_data.decode('base64').decode('latin1')
        self.assertEqual(
            test_fatt_content.replace('\n', ''), xml_content.replace('\n', ''))

    def test_0_xml_import(self):
        cr, uid = self.cr, self.uid
        # import source invoice
        res = self.run_import_invoice_wizard(
            'test0', 'IT05979361218_002.xml.p7m')
        invoice_id = res.get('domain')[0][2][0]
        # import metadata
        # check metadata file name is case insensitive
        res_notif = self.run_import_notif_wizard(
            'IT05979361218_002_MT_001.XML')
        notif_id = res_notif.get('res_id')
        notification = self.notifications_model.browse(cr, uid, notif_id)
        self.assertEqual(notification.message_type, 'MT')
        invoice_data = self.attach_model.browse(
            cr, uid, notification.fatturapa_in_attachment_id.id)
        self.assertEqual(invoice_data.file_identifier, 'IT05979361218_002')
        self.assertEqual(invoice_data.sdi_identifier, 5199973)
        # create accept notifications
        self.run_send_notif_wizard('accept', invoice_id)
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        attachment = self.notifications_model.browse(
            cr, uid, invoice.result_notification_id.id)
        # check notification
        xml_content = attachment.datas.decode('base64').decode('latin1')
        self.check_content(xml_content, 'IT05979361218_002_EC_002.xml')

    def test_1_xml_import(self):
        cr, uid = self.cr, self.uid
        # import source invoice
        res = self.run_import_invoice_wizard(
            'test1', 'IT02780790107_11007.xml')
        invoice_id = res.get('domain')[0][2][0]
        # import metadata
        # check metadata file name is case insensitive
        res_notif = self.run_import_notif_wizard(
            'IT02780790107_11007_MT_001.xml')
        notif_id = res_notif.get('res_id')
        notification = self.notifications_model.browse(cr, uid, notif_id)
        self.assertEqual(notification.message_type, 'MT')
        invoice_data = self.attach_model.browse(
            cr, uid, notification.fatturapa_in_attachment_id.id)
        self.assertEqual(invoice_data.file_identifier, 'IT02780790107_11007')
        self.assertEqual(invoice_data.sdi_identifier, 5199979)
        # create reject notifications
        self.run_send_rej_notif_wizard('rejected', invoice_id)
        invoice = self.invoice_model.browse(cr, uid, invoice_id)
        attachment = self.notifications_model.browse(
            cr, uid, invoice.result_notification_id.id)
        # check notification
        xml_content = attachment.datas.decode('base64').decode('latin1')
        self.check_content(xml_content, 'IT02780790107_11007_EC_002.xml')
        # check if rejected field is True and invoice is cancelled
        self.assertEqual(invoice.rejected, True)
        self.assertEqual(invoice.state, 'cancel')
        self.assertRaises(
            except_orm, invoice.action_cancel_draft
        )
