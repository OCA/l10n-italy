# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>

import logging
import re
import base64
import zipfile
import io

from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

FATTURAPA_IN_REGEX = '^(IT[a-zA-Z0-9]{11,16}|'\
                     '(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})'\
                     '_[a-zA-Z0-9]{1,5}'\
                     '\\.(xml|XML|Xml|zip|ZIP|Zip|p7m|P7M|P7m)'\
                     '(\\.(p7m|P7M|P7m))?$'
RESPONSE_MAIL_REGEX = '(IT[a-zA-Z0-9]{11,16}|'\
                      '(?!IT)[A-Z]{2}[a-zA-Z0-9]{2,28})'\
                      '_[a-zA-Z0-9]{1,5}'\
                      '_MT_[a-zA-Z0-9]{,3}'

fatturapa_regex = re.compile(FATTURAPA_IN_REGEX)
response_regex = re.compile(RESPONSE_MAIL_REGEX)


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
            fatturapa_attachments = [x for x in message_dict['attachments']
                                     if fatturapa_regex.match(x.fname)]
            response_attachments = [x for x in message_dict['attachments']
                                    if response_regex.match(x.fname)]
            if response_attachments and fatturapa_attachments:
                return self.manage_pec_fe_attachments(
                    message, message_dict, response_attachments)
            else:
                return self.manage_pec_sdi_notification(message, message_dict)

        elif self._context.get('fetchmail_server_id', False):
            # This is not an email coming from SDI
            fetchmail_server = self.env['fetchmail.server'].browse(
                self._context['fetchmail_server_id'])
            if fetchmail_server.is_fatturapa_pec:
                att = self.find_attachment_by_subject(message_dict['subject'])
                if att:
                    return self.manage_pec_sdi_response(att, message_dict)
                raise UserError(_(
                    "PEC message \"%s\" has been read "
                    "but not processed, as not related to an "
                    "e-invoice.\n"
                    "Please check PEC mailbox %s, at server %s,"
                    " with user %s."
                ) % (
                    message_dict['subject'],
                    fetchmail_server.name, fetchmail_server.server,
                    fetchmail_server.user
                ))
        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)

    def manage_pec_sdi_response(self, att, message_dict):
        # This is a PEC response (CONSEGNA o ACCETTAZIONE)
        # related to a message sent to SDI by us
        message_dict['model'] = 'fatturapa.attachment.out'
        message_dict['res_id'] = att.id
        self.clean_message_dict(message_dict)
        self.env['mail.message'].with_context(
            message_create_from_mail_mail=True).create(
            message_dict)
        return []

    def manage_pec_sdi_notification(self, message, message_dict):
        # this is an SDI notification
        message_dict = self.env['fatturapa.attachment.out'] \
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

    def manage_pec_fe_attachments(self, message, message_dict,
                                  response_attachments):
        # this is an electronic invoice
        if len(response_attachments) > 1:
            _logger.info(
                'More than 1 message found in mail of incoming invoice')
        message_dict['model'] = 'fatturapa.attachment.in'
        message_dict['record_name'] = message_dict['subject']
        message_dict['res_id'] = 0
        attachment_ids = self._message_post_process_attachments(
            message_dict['attachments'], [], message_dict)
        for attachment in self.env['ir.attachment'].browse(
                [att_id for m, att_id in attachment_ids]):
            if fatturapa_regex.match(attachment.name):
                self.create_fatturapa_attachment_in(attachment, message_dict)
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

    def find_attachment_by_subject(self, subject):
        attachment_out_model = self.env['fatturapa.attachment.out']
        if 'CONSEGNA: ' in subject:
            att_name = subject.replace('CONSEGNA: ', '')
            fatturapa_attachment_out = attachment_out_model \
                .search([
                    ('datas_fname', '=', att_name)
                ])
            if not fatturapa_attachment_out:
                fatturapa_attachment_out = attachment_out_model \
                    .search([
                        ('name', '=', att_name)
                    ])
            if len(fatturapa_attachment_out) == 1:
                return fatturapa_attachment_out
        if 'ACCETTAZIONE: ' in subject:
            att_name = subject.replace('ACCETTAZIONE: ', '')
            fatturapa_attachment_out = attachment_out_model \
                .search([
                    ('datas_fname', '=', att_name)
                ])
            if not fatturapa_attachment_out:
                fatturapa_attachment_out = attachment_out_model \
                    .search([
                        ('name', '=', att_name)
                    ])
            if len(fatturapa_attachment_out) == 1:
                return fatturapa_attachment_out
        return attachment_out_model.browse()

    def create_fatturapa_attachment_in(self, attachment, message_dict=None):
        decoded = base64.b64decode(attachment.datas)
        fatturapa_attachment_in = self.env['fatturapa.attachment.in']
        fetchmail_server_id = self.env.context.get('fetchmail_server_id')
        received_date = False
        if message_dict is not None and 'date' in message_dict:
            received_date = message_dict['date']
        company_id = False
        e_invoice_user_id = False
        # The incoming supplier e-bill doesn't carry which company
        # we must use to create the given fatturapa.attachment.in record,
        # so we expect fetchmail_server_id coming in the context
        # see fetchmail.py.
        # With this information we search which SDI is actually using it,
        # finally the SDI contain both company and user we would need to use
        if fetchmail_server_id:
            sdi_chan = self.env['sdi.channel'].search([
                ('fetch_pec_server_id', '=', fetchmail_server_id)], limit=1)
            if sdi_chan:
                # See check_fetch_pec_server_id
                company_id = sdi_chan.company_id.id
                e_invoice_user_id = sdi_chan.company_id.e_invoice_user_id.id
        if e_invoice_user_id:
            fatturapa_attachment_in = fatturapa_attachment_in.sudo(
                e_invoice_user_id)
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
                                'datas': base64.encodestring(inv_file.read()),
                                'company_id': company_id,
                                'e_invoice_received_date': received_date,
                            })
        else:
            fatturapa_atts = fatturapa_attachment_in.search(
                [('name', '=', attachment.name)])
            if fatturapa_atts:
                _logger.info(
                    "Invoice xml already processed in %s"
                    % fatturapa_atts.mapped('name'))
            else:
                fatturapa_attachment_in.create({
                    'ir_attachment_id': attachment.id,
                    'company_id': company_id,
                    'e_invoice_received_date': received_date,
                })
