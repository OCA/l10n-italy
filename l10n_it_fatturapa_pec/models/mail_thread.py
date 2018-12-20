# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re
import base64
import zipfile
import io

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

FATTURAPA_ACCOUNT = "@pec.fatturapa.it"
FATTURAPA_IN_REGEX = "^[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}.(xml|zip)"
RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}' \
                      '_MT_[a-zA-Z0-9]{,3}'


class MailThread(orm.AbstractModel):
    _inherit = 'mail.thread'

    def _create_message_attachments(self, cr, uid, message_dict, context=None):
        ir_attachment_obj = self.pool.get('ir.attachment')
        attachment_ids = []
        for name, content in message_dict['attachments']:
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            data_attach = {
                'name': name,
                'datas': base64.b64encode(str(content)),
                'datas_fname': name,
                'description': name,
                'res_model': message_dict.get('model', False),
                'res_id': message_dict.get('res_id', False),
            }
            attachment_ids.append(ir_attachment_obj.create(
                cr, uid, data_attach, context=context))
        return attachment_ids

    def _clean_message_dict(self, message_dict):
        del message_dict['attachments']
        del message_dict['cc']
        del message_dict['from']
        del message_dict['to']

    def message_route(self, cr, uid, message, model=None, thread_id=None,
                      custom_values=None, context=None):
        if any(FATTURAPA_ACCOUNT in x for x in [
            message.get('Reply-To', ''),
            message.get('From', ''),
            message.get('Return-Path', '')]
        ):
            _logger.info("Processing FatturaPA PEC with Message-Id: {}".format(
                message.get('Message-Id')))

            message_dict = self.message_parse(
                cr, uid, message, save_original=True, context=context)

            fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
            fatturapa_attachments = [a for a in message_dict['attachments'] if
                                     fatturapa_regex.match(a[0])]
            response_regex = re.compile(RESPONSE_MAIL_REGEX)
            response_attachments = [a for a in message_dict['attachments'] if
                                    response_regex.match(a[0])]
            if response_attachments and fatturapa_attachments:
                # this is an electronic invoice
                if len(response_attachments) > 1:
                    _logger.info('More than 1 message found in mail of '
                                 'incoming invoice')
                message_dict['model'] = 'fatturapa.attachment.in'
                message_dict['record_name'] = message_dict['subject']
                message_dict['res_id'] = 0

                attachment_ids = self._create_message_attachments(
                    cr, uid, message_dict, context=context)
                for attachment in self.pool.get('ir.attachment').browse(
                    cr, uid, attachment_ids, context=context):
                    if fatturapa_regex.match(attachment.name):
                        self.create_fatturapa_attachment_in(
                            cr, uid, attachment, context=context)

                message_dict['attachment_ids'] = [(6, 0, attachment_ids)]
                self._clean_message_dict(message_dict)

                # model and res_id are only needed by
                # _message_post_process_attachments: we don't attach to
                del message_dict['model']
                del message_dict['res_id']

                self.pool.get('mail.message').create(cr, uid, message_dict,
                                                     context=context)

                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

            else:
                # this is an SDI notification
                message_dict = self.pool.get('fatturapa.attachment.out').\
                    parse_pec_response(cr, uid, message_dict, context=context)

                message_dict['record_name'] = message_dict['subject']
                attachment_ids = self._create_message_attachments(
                    cr, uid, message_dict, context=context)
                message_dict['attachment_ids'] = [(6, 0, attachment_ids)]
                self._clean_message_dict(message_dict)

                self.pool.get('mail.message').create(
                    cr, uid, message_dict, context=context)
                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

        elif context.get('fetchmail_server_id', False):
            fetchmail_server_id = self.pool.get('fetchmail.server').browse(
                cr, uid, context['fetchmail_server_id'],
                context=context)
            if fetchmail_server_id.is_fatturapa_pec:
                message_dict = self.message_parse(
                    cr, uid, message, save_original=True, context=context)
                attachment_ids = self._create_message_attachments(
                    cr, uid, message_dict, context=context)
                message_dict['attachment_ids'] = [(6, 0, attachment_ids)]
                attachment_id = self.find_attachment_by_subject(
                    cr, uid, message_dict['subject'], context=context)
                if attachment_id:
                    message_dict['model'] = 'fatturapa.attachment.out'
                    message_dict['res_id'] = attachment_id
                    self._clean_message_dict(message_dict)
                    self.pool.get('mail.message').create(
                        cr, uid, message_dict, context=context)
                else:
                    self._clean_message_dict(message_dict)
                    self.pool.get('mail.message').create(
                        cr, uid, message_dict, context=context)
                    _logger.error('Can\'t route PEC E-Mail with Message-Id: {}'
                                  .format(message.get('Message-Id')))
                return []

        return super(MailThread, self).message_route(
            cr, uid, message, model=model, thread_id=thread_id,
            custom_values=custom_values, context=context)

    def find_attachment_by_subject(self, cr, uid, subject, context=None):
        if 'CONSEGNA: ' in subject:
            attachment_name = subject.replace('CONSEGNA: ', '')
            fatturapa_attachment_out_id = self.pool.get(
                'fatturapa.attachment.out').search(
                    cr, uid, [('datas_fname', '=', attachment_name)],
                    context=context)
            if len(fatturapa_attachment_out_id) == 1:
                return fatturapa_attachment_out_id[0]
        if 'ACCETTAZIONE: ' in subject:
            attachment_name = subject.replace('ACCETTAZIONE: ', '')
            fatturapa_attachment_out_id = self.pool.get(
                'fatturapa.attachment.out').search(
                    cr, uid, [('datas_fname', '=', attachment_name)],
                    context=context)
            if len(fatturapa_attachment_out_id) == 1:
                return fatturapa_attachment_out_id[0]
        return False

    def create_fatturapa_attachment_in(
            self, cr, uid, attachment, context=None):
        decoded = base64.b64decode(attachment.datas)
        fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
        fatturapa_attachment_in = self.pool.get('fatturapa.attachment.in')
        if attachment.file_type == 'application/zip':
            with zipfile.ZipFile(io.BytesIO(decoded)) as zf:
                for file_name in zf.namelist():
                    inv_file = zf.open(file_name)
                    if fatturapa_regex.match(file_name):
                        # check if this invoice is already
                        # in other fatturapa.attachment.in
                        fatturapa_attachment_ids = fatturapa_attachment_in.\
                            search(cr, uid, [('name', '=', file_name)],
                            context=context)
                        if fatturapa_attachment_ids:
                            _logger.info("In invoice %s already processed"
                                         % file_name)
                        else:
                            fatturapa_attachment_in.create({
                                    'name': file_name,
                                    'datas_fname': file_name,
                                    'datas': base64.encodestring(
                                        inv_file.read())
                                })
        else:
            fatturapa_attachment_ids = fatturapa_attachment_in.search(
                cr, uid, [('name', '=', attachment.name)],
                    context=context)
            if fatturapa_attachment_ids:
                _logger.info("Invoice xml already processed in %s" %
                             attachment.name)
            else:
                fatturapa_attachment_in.create(
                    cr, uid, {'ir_attachment_id': attachment.id},
                    context=context)
