# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#    Copyright 2014 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
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
##############################################################################

import email
from openerp import SUPERUSER_ID
from openerp.addons.mail.mail_message import decode
from openerp.osv import orm
from openerp.tools.translate import _
import xml.etree.ElementTree as ET


class MailThread(orm.Model):
    _inherit = 'mail.thread'

    def is_server_pec(self, cr, uid, context=None):
        if context is None:
            context = {}
        server_pool = self.pool.get('fetchmail.server')
        if 'fetchmail_server_id' in context:
            id = context.get('fetchmail_server_id')
            server = server_pool.read(cr, SUPERUSER_ID, [id], ['pec'])
            return server[0]['pec']
        return False

    def parse_daticert(self, cr, uid, daticert, context=None):
        msg_dict = {}
        root = ET.fromstring(daticert)
        message = None
        if 'tipo' in root.attrib:
            msg_dict['pec_type'] = root.attrib['tipo']
        if 'errore' in root.attrib:
            msg_dict['err_type'] = root.attrib['errore']
        for child in root:
            if child.tag == 'intestazione':
                for child2 in child:
                    if child2.tag == 'mittente':
                        msg_dict['email_from'] = child2.text
                    if child2.tag == 'destinatari':
                        recipient_id = self._message_find_partners_pec(
                            cr, uid, message, child2.text, context=context)
                        msg_dict['recipient_id'] = recipient_id
            if child.tag == 'dati':
                for child2 in child:
                    if child2.tag == 'msgid':
                        msg_dict['message_id'] = child2.text
                    if child2.tag == 'identificativo':
                        msg_dict['pec_msg_id'] = child2.text
        return msg_dict

    def get_pec_attachments(self, cr, uid, message, context=None):
        postacert = False
        daticert = False
        smime = False
        for part in message.walk():
            filename = part.get_param('filename', None, 'content-disposition')
            if not filename:
                filename = part.get_param('name', None)
            if filename:
                if isinstance(filename, tuple):
                    # RFC2231
                    filename = email.utils.collapse_rfc2231_value(
                        filename).strip()
                else:
                    filename = decode(filename)
            if (
                filename == 'postacert.eml' or
                filename == 'daticert.xml' or
                filename == 'smime.p7s'
            ):
                if part.is_multipart() and len(part.get_payload()) > 1:
                    raise orm.except_orm(
                        _('Error'),
                        _("Too many payloads for 'postacert.eml' or "
                          "'daticert.xml'. Not handled"))
                # http://goo.gl/zPRvxF
                if part.is_multipart():
                    # email.message.Message
                    attachment = part.get_payload()[0]
                else:
                    # string
                    attachment = part.get_payload(decode=True)
                if filename == 'postacert.eml':
                    postacert = attachment
                if filename == 'daticert.xml':
                    daticert = attachment
                if filename == 'smime.p7s':
                    smime = attachment
        return (postacert, daticert, smime)

    def message_parse(
        self, cr, uid, message, save_original=False, context=None
    ):
        if context is None:
            context = {}

        context['main_message_id'] = False
        context['pec_type'] = False
        if not self.is_server_pec(cr, uid, context=context):
            return super(MailThread, self).message_parse(
                cr, uid, message, save_original=save_original, context=context)
        message_pool = self.pool['mail.message']
        msg_dict = {}
        postacert, daticert, smime = self.get_pec_attachments(
            cr, uid, message, context=context)
        if not daticert:
            raise orm.except_orm(
                _('Error'), _('PEC message does not contain daticert.xml'))
        daticert_dict = self.parse_daticert(
            cr, uid, daticert, context=context)
        if daticert_dict.get('pec_type') == 'posta-certificata':
            if not postacert:
                raise orm.except_orm(
                    _('Error'),
                    _('PEC message does not contain postacert.eml'))
            msg_dict = super(MailThread, self).message_parse(
                cr, uid, postacert, save_original=False,
                context=context)
            msg_dict['attachments'] += [
                ('original_email.eml', message.as_string())]
        else:
            msg_dict = super(MailThread, self).message_parse(
                cr, uid, message, save_original=True,
                context=context)
        msg_dict.update(daticert_dict)
        msg_ids = []
        if (
            daticert_dict.get('message_id')
            and (
                daticert_dict.get('pec_type') != 'posta-certificata')
        ):
            msg_ids = message_pool.search(
                cr, uid, [('message_id', '=', daticert_dict['message_id'])],
                context=context)
            if len(msg_ids) > 1:
                raise orm.except_orm(
                    _('Error'),
                    _('Too many existing mails with message_id %s')
                    % daticert_dict['message_id'])
            if msg_ids:
                # I'm going to set this message as notification of the original
                # message and remove the message_id of this message
                # (it would be duplicated)
                context['main_message_id'] = msg_ids[0]
                context['pec_type'] = daticert_dict.get('pec_type')
            del msg_dict['message_id']
        #if message transport resend original mail with
        #transport error , marks in original message with
        #error, and after the server not save the original message
        #because is duplicate
        if (
            daticert_dict.get('message_id')
            and message['X-Trasporto'] == 'errore'
        ):
            msg_ids = message_pool.search(
                cr, uid, [('message_id', '=', daticert_dict['message_id'])],
                context=context)
            if len(msg_ids) > 1:
                raise orm.except_orm(
                    _('Error'),
                    _('Too many existing mails with message_id %s')
                    % daticert_dict['message_id'])
            else:
                message_pool = self.pool['mail.message']
                message_pool.write(
                    cr, uid, msg_ids, {
                        'error': True,
                    }, context=context)

        author_id = self._message_find_partners_pec(
            cr, uid, message, daticert_dict.get('email_from'), context=context)
        if author_id:
            msg_dict['author_id'] = author_id
        else:
            msg_dict['author_id'] = self.pool.get('res.partner').create(
                cr, SUPERUSER_ID,
                {
                    'name': daticert_dict.get('email_from'),
                    'pec_mail': daticert_dict.get('email_from')
                },context = context)
        msg_dict['server_id'] = context.get('fetchmail_server_id')

        return msg_dict

    def _message_find_partners_pec(
        self, cr, uid, message=None, email_from=False, context=None
    ):
        """
        create new method to search partner because
        the data of from  field of messagase is not found
        with _message_find_partners
        """
        res = False
        if email_from:
            partner_obj = self.pool.get('res.partner')
            partner_ids = partner_obj.search(
                cr, uid, [('pec_mail', '=', email_from.strip())],
                context=context)
            if partner_ids:
                res = partner_ids[0]
        return res
