# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
import re
import base64
import zipfile
import io

from odoo import api, models, _

_logger = logging.getLogger(__name__)

FATTURAPA_IN_REGEX = "^[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}.(xml|zip)"
RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_MT_' \
                      '[a-zA-Z0-9]{,3}'


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def clean_message_dict(self, message_dict):
        del message_dict['attachments']
        del message_dict['cc']
        del message_dict['from']
        del message_dict['to']

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):
        if any("@pec.fatturapa.it" in x for x in [
            message.get('Reply-To', ''),
            message.get('From', ''),
            message.get('Return-Path', '')]
        ):
            _logger.info("Processing FatturaPA PEC with Message-Id: "
                         "{}".format(message.get('Message-Id')))

            fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
            fatturapa_attachments = [x for x in message_dict['attachments']
                                     if fatturapa_regex.match(x.fname)]
            response_regex = re.compile(RESPONSE_MAIL_REGEX)
            response_attachments = [x for x in message_dict['attachments']
                                    if response_regex.match(x.fname)]
            if response_attachments and fatturapa_attachments:
                # this is an electronic invoice
                if len(response_attachments) > 1:
                    _logger.info(
                        'More than 1 message found in mail of incoming '
                        'invoice')
                message_dict['model'] = 'fatturapa.attachment.in'
                message_dict['record_name'] = message_dict['subject']
                message_dict['res_id'] = 0
                attachment_ids = self._message_post_process_attachments(
                    message_dict['attachments'], [], message_dict)
                for attachment in self.env['ir.attachment'].browse(
                        [att_id for m, att_id in attachment_ids]):
                    if fatturapa_regex.match(attachment.name):
                        self.create_fatturapa_attachment_in(attachment)

                message_dict['attachment_ids'] = attachment_ids
                self.clean_message_dict(message_dict)

                # model and res_id are only needed by
                # _message_post_process_attachments: we don't attach to
                del message_dict['model']
                del message_dict['res_id']

                # message_create_from_mail_mail to avoid to notify message
                # (see mail.message.create)
                self.env['mail.message'].with_context(
                    message_create_from_mail_mail=True).create(message_dict)
                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

            else:
                # this is an SDI notification
                message_dict = self.env['fatturapa.attachment.out']\
                    .parse_pec_response(message_dict)

                message_dict['record_name'] = message_dict['subject']
                attachment_ids = self._message_post_process_attachments(
                    message_dict['attachments'], [], message_dict)
                message_dict['attachment_ids'] = attachment_ids
                self.clean_message_dict(message_dict)

                # message_create_from_mail_mail to avoid to notify message
                # (see mail.message.create)
                self.env['mail.message'].with_context(
                    message_create_from_mail_mail=True).create(message_dict)
                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

        elif self._context.get('fetchmail_server_id', False):
            # This is not an email coming from SDI
            fetchmail_server = self.env['fetchmail.server'].browse(
                self._context['fetchmail_server_id'])
            if fetchmail_server.is_fatturapa_pec:
                att = self.find_attachment_by_subject(message_dict['subject'])
                if att:
                    # This a PEC response (CONSEGNA o ACCETTAZIONE)
                    # related to a message sent to SDI by us
                    message_dict['model'] = 'fatturapa.attachment.out'
                    message_dict['res_id'] = att.id
                    self.clean_message_dict(message_dict)
                    self.env['mail.message'].with_context(
                        message_create_from_mail_mail=True).create(
                            message_dict)
                else:
                    _logger.info(
                        'Can\'t route PEC E-Mail with Message-Id: {}'.format(
                            message.get('Message-Id'))
                    )
                    if fetchmail_server.e_inv_notify_partner_ids:
                        self.env['mail.mail'].create({
                            'subject': _(
                                "PEC message [%s] not processed"
                            ) % message.get('Subject'),
                            'body_html': _(
                                "<p>"
                                "PEC message with Message-Id %s has been read "
                                "but not processed, as not related to an "
                                "e-invoice.</p>"
                                "<p>Please check PEC mailbox %s, at server %s,"
                                " with user %s</p>"
                            ) % (
                                message.get('Message-Id'),
                                fetchmail_server.name, fetchmail_server.server,
                                fetchmail_server.user
                            ),
                            'recipient_ids': [(
                                6, 0,
                                fetchmail_server.e_inv_notify_partner_ids.ids
                            )]
                        })
                        _logger.info(
                            'Notifying partners %s about message with '
                            'Message-Id: %s' % (
                                fetchmail_server.e_inv_notify_partner_ids.ids,
                                message.get('Message-Id')))
                    else:
                        _logger.error(
                            'Can\'t notify anyone about not processed '
                            'PEC E-Mail with Message-Id: {}'.format(
                                message.get('Message-Id')))
                return []

        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)

    def find_attachment_by_subject(self, subject):
        if 'CONSEGNA: ' in subject:
            att_name = subject.replace('CONSEGNA: ', '')
            fatturapa_attachment_out = self.env[
                'fatturapa.attachment.out'
            ].search([('datas_fname', '=', att_name)])
            if len(fatturapa_attachment_out) == 1:
                return fatturapa_attachment_out
        if 'ACCETTAZIONE: ' in subject:
            att_name = subject.replace('ACCETTAZIONE: ', '')
            fatturapa_attachment_out = self.env[
                'fatturapa.attachment.out'
            ].search([('datas_fname', '=', att_name)])
            if len(fatturapa_attachment_out) == 1:
                return fatturapa_attachment_out
        return False

    def create_fatturapa_attachment_in(self, attachment):
        decoded = base64.b64decode(attachment.datas)
        fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
        fatturapa_attachment_in = self.env['fatturapa.attachment.in']
        if attachment.mimetype == 'application/zip':
            with zipfile.ZipFile(io.BytesIO(decoded)) as zf:
                for file_name in zf.namelist():
                    inv_file = zf.open(file_name)
                    if fatturapa_regex.match(file_name):
                        # check if this invoice is already
                        # in other fatturapa.attachment.in
                        fatturapa_atts = fatturapa_attachment_in.search([
                            ('name', '=', file_name)])
                        if fatturapa_atts:
                            _logger.info("In invoice %s already processed"
                                         % fatturapa_atts.mapped('name'))
                        else:
                            fatturapa_attachment_in.create({
                                'name': file_name,
                                'datas_fname': file_name,
                                'datas': base64.encodestring(inv_file.read())})
        else:
            fatturapa_atts = fatturapa_attachment_in.search(
                [('name', '=', attachment.name)])
            if fatturapa_atts:
                _logger.info(
                    "Invoice xml already processed in %s"
                    % fatturapa_atts.mapped('name'))
            else:
                fatturapa_attachment_in.create({
                    'ir_attachment_id': attachment.id})
