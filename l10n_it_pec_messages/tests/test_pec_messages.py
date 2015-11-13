# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    About license see __openerp__.py
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
        self.mail_model = self.registry('mail.mail')
        self.fetchmail_model = self.registry('fetchmail.server')
        self.compose_msg_model = self.registry('mail.compose.message')

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
        imap_server_id = self.ref('l10n_it_pec_messages.imap_pec_server')
        self.fetchmail_model.write(cr, uid, [imap_server_id], {
            'force_create_partner_from_mail': True,
            })
        self.thread_model.message_process(
            cr, uid, None, msg_file, save_original=False,
            strip_attachments=False, context=fetch_context)
        msg_ids = self.message_model.search(
            cr, uid, [
                ('pec_msg_id', '=',
                    'opec275.20141127151216.06559.08.1.17@pec.aruba.it')])
        self.assertEqual(len(msg_ids), 1)
        msg = self.message_model.browse(cr, uid, msg_ids[0])
        self.assertEqual(msg.author_id.name, u'thinkstudio@pec.it')
        self.assertEqual(msg.email_from, 'thinkstudio@pec.it')
        context = {
            'lang': 'en_US',
            'search_disable_custom_filters': True,
            'new_pec_mail': True,
            'tz': False,
            'uid': 1,
            'show_pec_email': True,
            'active_model': 'mail.message',
            'reply_pec': True,
            'default_composition_mode': 'reply',
            'pec_messages': True,
            'default_partner_ids': [msg.author_id.id],
            'active_ids': msg_ids,
            'active_id': msg_ids[0],
            }
        wizard_id = self.compose_msg_model.create(
            cr, uid, {'body': u'<p>replying to message2</p>'}, context=context)
        self.compose_msg_model.send_mail(cr, uid, [wizard_id], context=context)
        sent_msg_ids = self.registry('mail.mail').search(
            cr, uid, [('parent_id', '=', msg_ids[0])])
        self.assertEqual(len(sent_msg_ids), 1)
        sent_msg = self.mail_model.browse(cr, uid, sent_msg_ids[0])
        self.assertEqual(sent_msg.pec_type, 'posta-certificata')
        # setting message_id according to test data about
        # delivery and reception messages
        sent_msg.write({
            'message_id': "<1415985992.182905912399292.346704098667155-"
                          "openerp-private@elbati-Vostro-3550>"
            })

        # accettazione
        self.thread_model.message_process(
            cr, uid, None, accettazione_msg_file, save_original=False,
            strip_attachments=False, context=fetch_context)
        accettazione_msg_ids = self.message_model.search(
            cr, uid, [
                ('pec_msg_id', '=',
                    'opec275.20141114182632.23219.07.1.48@pec.aruba.it'),
                ('pec_type', '=', 'accettazione')])
        self.assertEqual(len(accettazione_msg_ids), 1)
        accettazione_msg = self.message_model.browse(
            cr, uid, accettazione_msg_ids[0])
        self.assertEqual(
            accettazione_msg.pec_msg_parent_id.id, sent_msg.mail_message_id.id)
        self.assertEqual(accettazione_msg.err_type, 'nessuno')
        # no delivery message received yet
        sent_msg.refresh()
        self.assertEqual(sent_msg.message_ok, False)

        # consegna
        self.thread_model.message_process(
            cr, uid, None, consegna_msg_file, save_original=False,
            strip_attachments=False, context=fetch_context)
        consegna_msg_ids = self.message_model.search(
            cr, uid, [
                ('pec_msg_id', '=',
                    'opec275.20141114182632.23219.07.1.48@pec.aruba.it'),
                ('pec_type', '=', 'avvenuta-consegna')])
        consegna_msg = self.message_model.browse(
            cr, uid, consegna_msg_ids[0])
        self.assertEqual(
            consegna_msg.pec_msg_parent_id.id, sent_msg.mail_message_id.id)
        self.assertEqual(consegna_msg.err_type, 'nessuno')
        self.assertEqual(len(consegna_msg_ids), 1)
        # delivery and reception messages received
        sent_msg.refresh()
        self.assertEqual(sent_msg.message_ok, True)
