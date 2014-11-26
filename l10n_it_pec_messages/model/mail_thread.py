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
import logging
import re

from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.mail.mail_message import decode
from openerp.osv import orm
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


mail_header_msgid_re = re.compile('<[^<>]+>')


class mail_thread(orm.Model):
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

    def _message_find_partners(
        self, cr, uid, message, header_fields=['From'], context=None
    ):
        """ Find partners related to some header fields of the message.

            TDE TODO: merge me with other partner finding methods in 8.0 """
        if not self.is_server_pec(cr, uid, context=context):
            return super(mail_thread, self)._message_find_partners(
                cr, uid, message, header_fields, context=context)
        else:
            partner_obj = self.pool.get('res.partner')
            partner_ids = []
            s = ', '.join(
                [decode(message.get(h))
                    for h in header_fields if message.get(h)])
            for email_address in tools.email_split(s):
                related_partners = partner_obj.search(
                    cr, uid, [
                        ('pec_mail', '=ilike', email_address),
                        ('user_ids', '!=', False)
                    ], limit=1, context=context)
                if not related_partners:
                    related_partners = partner_obj.search(
                        cr, uid, [('pec_mail', '=ilike', email_address)],
                        limit=1, context=context)
                partner_ids += related_partners
            return partner_ids

    # need to write new method  payload beacuse the original method
    # not heve context .
    def _message_extract_payload_pec(
        self, message, save_original=False, context=None
    ):
        """Extract body as HTML and attachments from the mail message"""
        attachments = []
        body = u''
        # TODO verify.. not correct for pec , pec mail have postacert.eml
        if save_original:
            attachments.append(('original_email.eml', message.as_string()))

        # Be careful, content-type may contain tricky content like in the
        # following example so test the MIME type with startswith()
        #
        # Content-Type: multipart/related;
        #   boundary="_004_3f1e4da175f349248b8d43cdeb9866f1AMSPR06MB343eurprd06pro_";
        #   type="text/html"
        # ~ import pdb;pdb.set_trace()
        if not message.is_multipart() or message.get(
            'content-type', ''
        ).startswith("text/"):
            encoding = message.get_content_charset()
            body = message.get_payload(decode=True)
            body = tools.ustr(body, encoding, errors='replace')
            if message.get_content_type() == 'text/plain':
                # text/plain -> <pre/>
                body = tools.append_content_to_html(u'', body, preserve=True)
        else:
            keepmsg = False
            mixed = False
            html = u''
            boundary_eml = ''
            boundary_eml_end = boundary_eml + '--'
            for part in message.walk():
                # TODO find contet_type
                # multipart/mixed; boundary="----------=_1416483046-5019-25"
                #  _1416483046-5019-25 e' il codice di confine delle parti
                # del messaggio
                #  multipart/signed; protocol="application/x-pkcs7-signature";
                #  application/xml; name="daticert.xml"
                #  message/rfc822; name="postacert.eml"
                #  application/x-pkcs7-signature; name="smime.p7s"
                #
                if part.get_content_type() == 'multipart/rfc822':
                    keepmsg = True

                if not mixed and part.get_content_type() == 'multipart/mixed':
                    mixed = True
                    boundary_eml = part.get_boundary()
                    boundary_eml_end = '--'+part.get_boundary()+'--'
                if part.get_content_maintype() == 'multipart':
                    continue  # skip container

                filename = part.get_param(
                    'filename', None, 'content-disposition')
                if not filename:
                    filename = part.get_param('name', None)
                if filename:
                    if isinstance(filename, tuple):
                        # RFC2231
                        filename = email.utils.collapse_rfc2231_value(
                            filename).strip()
                    else:
                        filename = decode(filename)
                encoding = part.get_content_charset()  # None if attachment

                # 1) Find eml bound and create -> attachments
                if filename and part.get_content_type() == 'message/rfc822':
                    dat = message.as_string().split(boundary_eml_end)[0].split(
                        boundary_eml)[4].split('\n\n', 1)[1]
                    attachments.append((filename, dat))
                    continue
                # 1a) Explicit Attachments -> attachments
                if filename or part.get(
                    'content-disposition', ''
                ).strip().startswith('attachment'):
                    attachments.append(
                        (filename or 'attachment', part.get_payload(
                            decode=True)))
                    continue

                # 2) text/plain -> <pre/>
                if part.get_content_type() == 'text/plain' and (keepmsg):
                    body = tools.append_content_to_html(body, tools.ustr(
                        part.get_payload(decode=True),
                        encoding, errors='replace'), preserve=True)
                # 3) text/html -> raw
                elif part.get_content_type() == 'text/html':
                    # mutlipart/signed have one text and a html part,
                    # keep only the second
                    # mixed allows several html parts, append html content
                    append_content = keepmsg
                    html = tools.ustr(
                        part.get_payload(decode=True), encoding,
                        errors='replace')
                    if not append_content:
                        body = html
                    else:
                        body = tools.append_content_to_html(
                            body, html, plaintext=False)
        return body, attachments

    def message_parse(
        self, cr, uid, message, save_original=False, context=None
    ):
        msg_dict = super(mail_thread, self).message_parse(
            cr, uid, message, save_original=save_original, context=context)
        if not self.is_server_pec(cr, uid, context=context):
            return msg_dict

        # Envelope fields not stored in mail.message but made available
        # for message_new()
        msg_dict['from'] = decode(message.get('Return-Path'))

        if message.get('Reply-To'):
            author_ids = self._message_find_partners(
                cr, uid, message, ['Return-Path'], context=context)
            if author_ids:
                msg_dict['author_id'] = author_ids[0]
            msg_dict['email_from'] = decode(message.get('Return-Path'))
        partner_ids = self._message_find_partners(
            cr, uid, message, ['To', 'Cc'], context=context)
        msg_dict['partner_ids'] = [
            (4, partner_id) for partner_id in partner_ids
            ]

        if message.get('In-Reply-To'):
            parent_ids = self.pool.get('mail.message').search(
                cr, uid, [('message_id', '=', decode(
                    message['In-Reply-To'].strip().split('<').split('>')))])
            if parent_ids:
                msg_dict['parent_id'] = parent_ids[0]

        msg_dict['server_id'] = context.get('fetchmail_server_id')
        msg_dict['pec_type'] = message.get('X-Tiporicevuta')
        msg_dict['pec_msg_id'] = message.get('Message-ID')
        msg_dict['ref_msg_id'] = message.get('X-Riferimento-Message-ID')
        msg_dict['body'], msg_dict[
            'attachments'
            ] = self._message_extract_payload_pec(
                message, save_original=save_original)
        return msg_dict
