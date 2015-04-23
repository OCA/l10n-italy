# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import openerp.tests.common as test_common
from openerp import addons


class TestPecMessages(test_common.SingleTransactionCase):

    def getFile(self, filename):
        path = addons.get_module_resource('l10n_it_pec_messages',
                                          'tests', 'data', filename)
        with open(path) as test_data:
            content = test_data.read()
        return content

    def setUp(self):
        super(TestPecMessages, self).setUp()
        self.thread_model = self.registry('mail.thread')
        self.message_model = self.registry('mail.message')
        self.fetchmail_model = self.registry('fetchmail.server')

    def test_message_1(self):
        cr, uid = self.cr, self.uid
        msg = self.getFile('message1')
        context = {
            'lang': 'en_US',
            'tz': False,
            'uid': 1,
            'fetchmail_cron_running': True,
            'server_type': u'imap',
            'fetchmail_server_id': 1,
            }
        self.thread_model.message_process(
            cr, uid, None, msg, save_original=False, strip_attachments=False,
            context=context)
        msg_ids = self.message_model.search(
            cr, uid, [
                ('pec_msg_id', '=',
                    'opec275.20141107165200.03048.08.1.17@pec.aruba.it')])
        self.assertEqual(len(msg_ids), 1)
        msg = self.message_model.browse(cr, uid, msg_ids[0])
        self.assertEqual(msg.pec_type, 'posta-certificata')
        self.assertEqual(msg.direction, 'in')
        imap_server_id = self.ref('l10n_it_pec_messages.imap_pec_server')
        self.assertEqual(msg.server_id.id, imap_server_id)
        self.assertEqual(msg.email_from, 'thinkstudio@pec.it')
        self.assertEqual(
            msg.message_id,
            u'<NEOEQO$8B558E13C0664DE7004C1EFB790D1A09@pec.it>')
        self.assertFalse(msg.author_id)

    def test_message_2_with_partner(self):
        cr, uid = self.cr, self.uid
        msg = self.getFile('message2')
        context = {
            'lang': 'en_US',
            'tz': False,
            'uid': 1,
            'fetchmail_cron_running': True,
            'server_type': u'imap',
            'fetchmail_server_id': 1,
            }
        imap_server_id = self.ref('l10n_it_pec_messages.imap_pec_server')
        self.fetchmail_model.write(cr, uid, [imap_server_id], {
            'force_create_partner_from_mail': True,
            })
        self.thread_model.message_process(
            cr, uid, None, msg, save_original=False, strip_attachments=False,
            context=context)
        msg_ids = self.message_model.search(
            cr, uid, [
                ('pec_msg_id', '=',
                    'opec275.20141127151216.06559.08.1.17@pec.aruba.it')])
        self.assertEqual(len(msg_ids), 1)
        msg = self.message_model.browse(cr, uid, msg_ids[0])
        self.assertEqual(msg.author_id.name, u'thinkstudio@pec.it')
        self.assertEqual(msg.email_from, 'thinkstudio@pec.it')
