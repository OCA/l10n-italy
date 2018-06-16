# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import email
import logging
from odoo import api, tools, models, _
from odoo.exceptions import UserError
import xml.etree.ElementTree as ET

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def is_server_pec(self):
        server_pool = self.env['fetchmail.server']
        if 'fetchmail_server_id' in self.env.context:
            srv_id = self.env.context.get('fetchmail_server_id')
            server = server_pool.sudo().browse(srv_id)
            return server.pec
        return False

    def parse_daticert(self, daticert):
        msg_dict = {}
        root = ET.fromstring(daticert)
        if 'tipo' in root.attrib:
            msg_dict['pec_type'] = root.attrib['tipo']
        if 'errore' in root.attrib:
            msg_dict['err_type'] = root.attrib['errore']
        for child in root:
            if child.tag == 'intestazione':
                for child2 in child:
                    if child2.tag == 'mittente':
                        msg_dict['email_from'] = child2.text
            if child.tag == 'dati':
                for child2 in child:
                    if child2.tag == 'msgid':
                        msg_dict['message_id'] = child2.text
                    if child2.tag == 'identificativo':
                        msg_dict['pec_msg_id'] = child2.text
                    if child2.tag == 'consegna':
                        recipient_ids = self._find_partner_from_emails([
                            child2.text
                        ])
                        if recipient_ids:
                            msg_dict['recipient_id'] = recipient_ids[0]
                        msg_dict['recipient_addr'] = child2.text
        return msg_dict

    def _get_msg_anomalia(self, msg):
        to = None
        msg_id = None
        parser = email.Parser.HeaderParser()
        msg_val = email.message_from_string(
            parser.parsestr(msg.as_string()).get_payload()
        )
        if 'To'in msg_val:
            to = msg_val['To']
        if 'X-Riferimento-Message-ID'in msg_val:
            msg_id = msg_val['X-Riferimento-Message-ID']
        return to, msg_id

    def _get_msg_delivery(self, msg):
        for dsn in msg.get_payload():
            if 'Action' in dsn:
                return dsn['Action']

    def _get_msg_payload(self, msg, parts=None, num=0):
        """
        This method recursively checks the message structure and
            saves the informations (bodies, attachments,
            pkcs7 signatures, etc.) in a dictionary.

        The method parameters are:

         - msg is the multipart message to process; the first time
         the method is called it is exactly the Original.eml message,
         that is: the email as it arrives from the imap server.
         The method is called recursively when a multipart structure is
         found, in this case msg is a multipart inside the Original.eml
         message and the num param is the depth of the multipart inside
         the Original.eml message.
         - parts is the dictionary where the informations are saved
         - num is an integer that refers to the depth
            of the msg content in the Original.eml message

        Some examples of the structure for the different kind of pec messages
        can be found in the docs folder of this module

        """
        if parts is None:
            parts = {}
        for part in msg.get_payload():
            filename = part.get_param('filename', None, 'content-disposition')
            if not filename:
                filename = part.get_param('name', None)
            if filename:
                if isinstance(filename, tuple):
                    # RFC2231
                    filename = email.utils.collapse_rfc2231_value(
                        filename).strip()
                else:
                    filename = tools.decode_smtp_header(filename)
            # Returns the files for a normal pec email
            if num == 0 and part.get_content_type() == \
                    'application/x-pkcs7-signature' and \
                    filename == 'smime.p7s':
                parts['smime.p7s'] = part.get_payload(decode=True)
            elif num == 1 and part.get_content_type() == \
                    'application/xml' and \
                    filename == 'daticert.xml':
                parts['daticert.xml'] = part.get_payload(decode=True)
            elif num == 1 and part.get_content_type() == \
                    'message/rfc822' and \
                    filename == 'postacert.eml':
                parts['postacert.eml'] = part.get_payload()[0]
            # If something went wrong: get basic info of the original message
            elif part.get_content_type() == \
                    'multipart/report':
                parts['report'] = True
            elif part.get_content_type() == \
                    'message/delivery-status':
                parts['delivery-status'] = self._get_msg_delivery(part)
            # If rfc822-headers is found get original msg info from payload
            elif part.get_content_type() == \
                    'text/rfc822-headers':
                parts['To'], parts['Msg_ID'] = \
                    self._get_msg_anomalia(part)
            # If no rfc822-headers than get info from original daticert.xml
            elif 'report' in parts and 'Msg_ID' not in parts and \
                    'daticert.xml' not in parts and \
                    part.get_content_type() == \
                    'application/xml' and \
                    filename == 'daticert.xml':
                origin_daticert = part.get_payload(decode=True)
                parsed_daticert = self.parse_daticert(origin_daticert)
                if 'recipient_addr' in parsed_daticert:
                    parts['To'] = parsed_daticert['recipient_addr']
                if 'msgid' in parsed_daticert:
                    parts['Msg_ID'] = parsed_daticert['msgid']
            else:
                pass
            # At last, if msg is multipart then call this method iteratively
            if part.is_multipart():
                parts = self._get_msg_payload(part, parts=parts, num=num + 1)
        return parts

    def _message_extract_payload_receipt(self, message,
                                         save_original=False):
        """Extract body as HTML and attachments from the mail message"""
        attachments = []
        body = u''
        if save_original:
            attachments.append(('original_email.eml', message.as_string()))
        if not message.is_multipart() or \
                'text/' in message.get('content-type', ''):
            encoding = message.get_content_charset()
            body = message.get_payload(decode=True)
            body = tools.ustr(body, encoding, errors='replace')
            if message.get_content_type() == 'text/plain':
                # text/plain -> <pre/>
                body = tools.append_content_to_html(u'', body, preserve=True)
        else:
            alternative = False
            for part in message.walk():
                if part.get_content_type() == 'multipart/alternative':
                    alternative = True
                if part.get_content_maintype() == 'multipart':
                    continue  # skip container
                filename = part.get_param('filename',
                                          None,
                                          'content-disposition')
                if not filename:
                    filename = part.get_param('name', None)
                if filename:
                    if isinstance(filename, tuple):
                        # RFC2231
                        filename = email.utils.collapse_rfc2231_value(
                            filename).strip()
                    else:
                        filename = tools.decode_smtp_header(filename)
                encoding = part.get_content_charset()  # None if attachment
                # 1) Explicit Attachments -> attachments
                if filename or part.get('content-disposition', '')\
                        .strip().startswith('attachment'):
                    attachments.append((filename or 'attachment',
                                        part.get_payload(decode=True))
                                       )
                    continue
                # 2) text/plain -> <pre/>
                if part.get_content_type() == 'text/plain' and \
                        (not alternative or not body):
                    body = tools.append_content_to_html(
                        body,
                        tools.ustr(part.get_payload(decode=True),
                                   encoding, errors='replace'),
                        preserve=True)
                # 3) text/html -> raw
                elif part.get_content_type() == 'text/html':
                    continue
                # 4) Anything else -> attachment
                else:
                    attachments.append((filename or 'attachment',
                                        part.get_payload(decode=True))
                                       )
        return body, attachments

    @api.model
    def message_parse(self, message, save_original=False):
        if not self.is_server_pec():
            return super(MailThread, self).message_parse(
                message, save_original=save_original)
        message_pool = self.env['mail.message']
        daticert_dict = {}
        parts = {}
        num = 0
        parts = self._get_msg_payload(message, parts=parts, num=num)
        daticert = 'daticert.xml' in parts and parts['daticert.xml'] or None
        postacert = 'postacert.eml' in parts and parts['postacert.eml'] or None
        if daticert:
            daticert_dict = self.parse_daticert(daticert)
        else:
            if 'To' not in parts and 'Msg_ID' not in parts:
                raise UserError(_('PEC message does not contain daticert.xml'))
            else:
                daticert_dict['recipient_addr'] = parts['To']
                daticert_dict['message_id'] = parts['Msg_ID']
                daticert_dict['pec_type'] = 'errore-consegna'
                daticert_dict['pec_msg_id'] = message['Message-ID']
                daticert_dict['err_type'] = 'no-dest'
                daticert_dict['email_from'] = message['From']
        if daticert_dict.get('pec_type') == 'posta-certificata':
            if not postacert:
                raise UserError(
                    _('PEC message does not contain postacert.eml'))
            msg_dict = super(MailThread, self).message_parse(
                postacert, save_original=False)
            msg_dict['attachments'] += [
                ('original_email.eml', message.as_string())]
        else:
            msg_dict = super(MailThread, self).message_parse(
                message, save_original=True)
            if daticert_dict.get('pec_type') in \
                    ('avvenuta-consegna', 'errore-consegna'):
                msg_dict['body'], attachs = \
                    self._message_extract_payload_receipt(
                    message,
                    save_original=save_original)
        msg_dict.update(daticert_dict)
        if (
            daticert_dict.get('message_id') and
            (
                daticert_dict.get('pec_type') != 'posta-certificata')
        ):
            msg_ids = message_pool.search(
                [('message_id', '=', daticert_dict['message_id'])])
            if len(msg_ids) > 1:
                raise UserError(
                    _('Too many existing mails with message_id %s')
                    % daticert_dict['message_id'])
            if msg_ids:
                # I'm going to set this message as notification of the original
                # message and remove the message_id of this message
                # (it would be duplicated)
                # before deletion check if this message is present and linked
                # with main massage id, if false remove message_id else no
                msg_dict['pec_msg_parent_id'] = msg_ids[0].id
                domain = [
                    ('pec_msg_id', '=', daticert_dict['pec_msg_id']),
                    ('pec_type', '=', daticert_dict.get('pec_type'))
                ]
                # if daticert_dict has a recipient_addr than we have to
                # add a domain condition so that we can ignore only
                # notification message that are already present in the system
                if daticert_dict.get('recipient_addr'):
                    domain.append(('recipient_addr',
                                   '=',
                                   daticert_dict.get('recipient_addr'))
                                  )
                chk_msgids = message_pool.search(domain)
                if not chk_msgids:
                    del msg_dict['message_id']
        # if message transport resend original mail with
        # transport error , marks the original message with
        # error, afterwards the server does not save the original message
        # because it is duplicate
        if (
            daticert_dict.get('message_id') and
            message['X-Trasporto'] == 'errore'
        ):
            msg_ids = message_pool.search(
                [('message_id', '=', daticert_dict['message_id'])])
            if len(msg_ids) > 1:
                raise UserError(
                    _('Too many existing emails with message_id %s')
                    % daticert_dict['message_id'])
            else:
                # TODO notify by email
                msg_ids[0].write({'pec_error': True})

        author_id = self._find_partner_from_emails(
            [daticert_dict.get('email_from')])
        if author_id:
            msg_dict['author_id'] = author_id[0]
        msg_dict['server_id'] = self.env.context.get('fetchmail_server_id')

        return msg_dict

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None,
        custom_values=None
    ):
        if message_dict.get('pec_type'):
            # override this to handle specific routing, like e-invoice
            message_id = message.get('Message-Id')
            message_dict['record_name'] = message_dict['subject']
            message_dict['model'] = 'mail.message'
            message_dict['res_id'] = 0
            attachment_ids = self._message_post_process_attachments(
                message_dict['attachments'], [], message_dict)
            message_dict['attachment_ids'] = attachment_ids
            del message_dict['attachments']
            del message_dict['cc']
            del message_dict['from']
            del message_dict['to']

            # model and res_id are only needed by
            # _message_post_process_attachments: we don't attach to
            del message_dict['model']
            del message_dict['res_id']

            # message_create_from_mail_mail to avoid to notify message
            # (see mail.message.create)
            self.env['mail.message'].with_context(
                message_create_from_mail_mail=True).create(message_dict)
            _logger.info(
                'Routing PEC with Message-Id: %s' % message_id
            )
            return []
        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values
        )
