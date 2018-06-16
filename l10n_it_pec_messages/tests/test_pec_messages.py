# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import openerp.tests.common as test_common
from odoo.modules.module import get_module_resource


class TestPecMessages(test_common.SingleTransactionCase):

    def getFile(self, filename):
        path = get_module_resource(
            'l10n_it_pec_messages',
            'tests', 'data', filename)
        with open(path) as test_data:
            content = test_data.read()
        return content

    def setUp(self):
        super(TestPecMessages, self).setUp()
        self.thread_model = self.env['mail.thread']
        self.message_model = self.env['mail.message']
        self.mail_model = self.env['mail.mail']
        self.fetchmail_model = self.env['fetchmail.server']
        self.compose_msg_model = self.env['mail.compose.message']
        self.pec_partner_1 = self.env.ref('l10n_it_pec_messages.pec_partner_1')
        self.pec_partner_2 = self.env.ref('l10n_it_pec_messages.pec_partner_2')

    def test_message_1(self):
        msg = self.getFile('message1')
        context = {
            'lang': 'en_US',
            'tz': False,
            'uid': 1,
            'fetchmail_cron_running': True,
            'server_type': u'imap',
            'fetchmail_server_id': 1,
            }
        self.thread_model.with_context(context).message_process(
            None, msg, save_original=False, strip_attachments=False)
        msg_ids = self.message_model.search([
            ('pec_msg_id', '=',
                'opec275.20141107165200.03048.08.1.17@pec.aruba.it')
        ])
        self.assertEqual(len(msg_ids), 1)
        msg = msg_ids[0]
        self.assertEqual(msg.pec_type, 'posta-certificata')
        self.assertEqual(msg.direction, 'in')
        imap_server = self.env.ref('l10n_it_pec_messages.imap_pec_server')
        self.assertEqual(msg.server_id.id, imap_server.id)
        self.assertEqual(msg.email_from, 'thinkstudio@pec.it')
        self.assertEqual(
            msg.message_id,
            u'<NEOEQO$8B558E13C0664DE7004C1EFB790D1A09@pec.it>')
        self.assertEqual(msg.author_id.id, self.pec_partner_1.id)
        self.assertFalse(self.pec_partner_1.is_server_pec())

    def test_message_2_with_partner(self):
        msg_file = self.getFile('message2')
        accettazione_msg_file = self.getFile('message2_accettazione')
        consegna_msg_file = self.getFile('message2_consegna')
        fetch_context = {
            'lang': 'en_US',
            'tz': False,
            'uid': 1,
            'fetchmail_cron_running': True,
            'server_type': u'imap',
            'fetchmail_server_id': 1,
            }
        imap_server = self.env.ref('l10n_it_pec_messages.imap_pec_server')
        self.thread_model.with_context(fetch_context).message_process(
            None, msg_file, save_original=False, strip_attachments=False)
        msg_ids = self.message_model.search([
            ('pec_msg_id', '=',
                'opec275.20141127151216.06559.08.1.17@pec.aruba.it')])
        self.assertEqual(len(msg_ids), 1)
        msg = msg_ids[0]
        self.assertEqual(msg.author_id.id, self.pec_partner_1.id)
        self.assertEqual(msg.email_from, 'thinkstudio@pec.it')
        context = {
            'lang': 'en_US',
            'tz': False,
            'uid': 1,
            'active_model': 'mail.message',
            'new_pec_mail': True,
            'default_partner_ids': [msg.author_id.id],
            }
        wizard_id = self.compose_msg_model.with_context(context).create({
            'body': u'<p>new message</p>',
            'server_id': imap_server.id,
            'author_id': self.pec_partner_2.id,
        })
        wizard_id.send_mail()
        sent_msg_ids = self.message_model.search([
            ('author_id', '=', self.pec_partner_2.id)
        ])
        self.assertEqual(len(sent_msg_ids), 1)
        self.assertEqual(
            sent_msg_ids[0].out_server_id.id,
            self.env.ref('l10n_it_pec_messages.smtp_pec_server').id)
        sent_msg_ids = self.mail_model.search([
            ('author_id', '=', self.pec_partner_2.id)
        ])
        self.assertEqual(len(sent_msg_ids), 1)
        sent_msg = sent_msg_ids[0]
        self.assertEqual(sent_msg.pec_type, 'posta-certificata')
        # setting message_id according to test data about
        # delivery and reception messages
        sent_msg.write({
            'message_id': "<1415985992.182905912399292.346704098667155-"
                          "openerp-private@elbati-Vostro-3550>"
            })

        # accettazione
        self.thread_model.with_context(fetch_context).message_process(
            None, accettazione_msg_file, save_original=False,
            strip_attachments=False)
        accettazione_msg_ids = self.message_model.search([
            ('pec_msg_id', '=',
                'opec275.20141114182632.23219.07.1.48@pec.aruba.it'),
            ('pec_type', '=', 'accettazione')
        ])
        self.assertEqual(len(accettazione_msg_ids), 1)
        accettazione_msg = accettazione_msg_ids[0]
        self.assertEqual(
            accettazione_msg.pec_msg_parent_id.id, sent_msg.mail_message_id.id)
        self.assertEqual(accettazione_msg.err_type, 'nessuno')
        # no delivery message received yet
        sent_msg.refresh()

        # consegna
        self.thread_model.with_context(fetch_context).message_process(
            None, consegna_msg_file, save_original=False,
            strip_attachments=False)
        consegna_msg_ids = self.message_model.search([
            ('pec_msg_id', '=',
                'opec275.20141114182632.23219.07.1.48@pec.aruba.it'),
            ('pec_type', '=', 'avvenuta-consegna')
        ])
        consegna_msg = consegna_msg_ids[0]
        self.assertEqual(
            consegna_msg.pec_msg_parent_id.id, sent_msg.mail_message_id.id)
        self.assertEqual(consegna_msg.err_type, 'nessuno')
        self.assertEqual(len(consegna_msg_ids), 1)
        # TODO increase coverage
