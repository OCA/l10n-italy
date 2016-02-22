# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014-2015 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#   About license see __openerp__.py
#
##############################################################################

import email
from openerp import SUPERUSER_ID
from openerp.addons.mail.mail_message import decode
from openerp.osv import orm
from openerp import tools
from openerp.tools.translate import _
import xml.etree.ElementTree as ET


class MailThread(orm.Model):
    _inherit = 'mail.thread'

    def is_server_pec(self, cr, uid, context=None):
        if context is None:
            context = {}
        server_pool = self.pool.get('fetchmail.server')
        if 'fetchmail_server_id' in context:
            srv_id = context.get('fetchmail_server_id')
            server = server_pool.read(cr, SUPERUSER_ID, [srv_id], ['pec'])
            return server[0]['pec']
        return False

    def force_create_partner(self, cr, uid, context=None):
        if context is None:
            context = {}
        server_pool = self.pool.get('fetchmail.server')
        if 'fetchmail_server_id' in context:
            srv_id = context.get('fetchmail_server_id')
            server = server_pool.browse(cr,
                                        SUPERUSER_ID,
                                        srv_id,
                                        context=context)
            if server:
                return server.force_create_partner_from_mail
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
            if child.tag == 'dati':
                for child2 in child:
                    if child2.tag == 'msgid':
                        msg_dict['message_id'] = child2.text
                    if child2.tag == 'identificativo':
                        msg_dict['pec_msg_id'] = child2.text
                    if child2.tag == 'consegna':
                        recipient_id = self._FindPartnersPec(
                            cr, uid, message, child2.text, context=context)
                        if recipient_id:
                            msg_dict['recipient_id'] = recipient_id
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

    def _get_msg_payload(self, cr, uid, msg, parts=None, num=0):
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
                    filename = decode(filename)
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
                parsed_daticert = self.parse_daticert(cr, uid, origin_daticert)
                if 'recipient_addr' in parsed_daticert:
                    parts['To'] = parsed_daticert['recipient_addr']
                if 'msgid' in parsed_daticert:
                    parts['Msg_ID'] = parsed_daticert['msgid']
            else:
                pass
            # At last, if msg is multipart then call this method iteratively
            if part.is_multipart():
                parts = self._get_msg_payload(cr, uid, part,
                                              parts=parts, num=num + 1)
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
                        filename = decode(filename)
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
        daticert_dict = {}
        parts = {}
        num = 0
        parts = self._get_msg_payload(cr, uid, message,
                                      parts=parts, num=num)
        daticert = 'daticert.xml' in parts and parts['daticert.xml'] or None
        postacert = 'postacert.eml' in parts and parts['postacert.eml'] or None
        if daticert:
            daticert_dict = self.parse_daticert(
                cr, uid, daticert, context=context)
        else:
            if 'To' not in parts and 'Msg_ID' not in parts:
                raise orm.except_orm(
                    _('Error'), _('PEC message does not contain daticert.xml'))
            else:
                daticert_dict['recipient_addr'] = parts['To']
                daticert_dict['message_id'] = parts['Msg_ID']
                daticert_dict['pec_type'] = 'errore-consegna'
                daticert_dict['pec_msg_id'] = message['Message-ID']
                daticert_dict['err_type'] = 'no-dest'
                daticert_dict['email_from'] = message['From']
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
            if daticert_dict.get('pec_type') in \
                    ('avvenuta-consegna', 'errore-consegna'):
                msg_dict['body'], attachs = \
                    self._message_extract_payload_receipt(
                    message,
                    save_original=save_original)
        msg_dict.update(daticert_dict)
        msg_ids = []
        if (
            daticert_dict.get('message_id') and
            (
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
                # before deletion check if this message is prensent and linked
                # with main massage id, if false remove message_id else no
                msg_dict['pec_msg_parent_id'] = msg_ids[0]
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
                chk_msgids = message_pool.search(
                    cr, uid,
                    domain,
                    context=context)
                if not chk_msgids:
                    context['main_message_id'] = msg_ids[0]
                    context['pec_type'] = daticert_dict.get('pec_type')
                    del msg_dict['message_id']
        # if message transport resend original mail with
        # transport error , marks in original message with
        # error, and after the server not save the original message
        # because is duplicate
        if (
            daticert_dict.get('message_id') and
            message['X-Trasporto'] == 'errore'
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

        author_id = self._FindOrCreatePartnersPec(
            cr, uid, message, daticert_dict.get('email_from'), context=context)
        if author_id:
            msg_dict['author_id'] = author_id
        msg_dict['server_id'] = context.get('fetchmail_server_id')

        return msg_dict

    def _FindPartnersPec(
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

    def _FindOrCreatePartnersPec(
        self, cr, uid, message=None, pec_address=False, context=None
    ):
        """
        search partner if not exit create it
        """
        res = self._FindPartnersPec(
            cr, uid, message, pec_address, context=context)
        if not res and self.force_create_partner(cr, uid, context):
            res = self.pool['res.partner'].create(
                cr, SUPERUSER_ID,
                {
                    'name': pec_address,
                    'pec_mail': pec_address
                }, context=context)
        return res
