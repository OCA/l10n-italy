# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import api, tools, exceptions, models, _

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = "^[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{5}\.(xml|zip)"


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):

        if any("@pec.fatturapa.it" in x for x in [
                    message.get('Reply-To'),
                    message.get('From'),
                    message.get('Return-Path')
        ]):
            _logger.info("Processing FatturaPA PEC Invoice with Message-Id: "
                         "{}".format(message.get('Message-Id')))
            message_dict, message_type = self.env['fatturapa.attachment.out']\
                .parse_pec_response(message_dict)
            if message_type == 'MT':
                message_dict['record_name'] = message_dict['subject']
                message_dict['model'] = 'mail.message'
                message_dict['res_id'] = 0
                attachment_ids = self._message_post_process_attachments(
                    message_dict['attachments'], [], message_dict)
                message_dict['attachment_ids'] = attachment_ids
                self.env['fatturapa.attachment.in']\
                    .parse_pec_attachment(attachment_ids)

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
                _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                             .format(message.get('Message-Id')))
                return []

        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)
