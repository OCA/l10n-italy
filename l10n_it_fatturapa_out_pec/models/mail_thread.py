# -*- coding: utf-8 -*-
# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):
        if any("@pec.fatturapa.it" in x for x in [
            message.get('Reply-To', ''),
            message.get('From', ''),
            message.get('Return-Path', '')]
        ):
            _logger.info("Processing FatturaPA PEC Response with Message-Id: "
                         "{}".format(message.get('Message-Id')))
            message_dict = self.env['fatturapa.attachment.out']\
                .parse_pec_response(message_dict)

            message_dict['record_name'] = message_dict['subject']
            attachment_ids = self._message_post_process_attachments(
                message_dict['attachments'], [], message_dict)
            message_dict['attachment_ids'] = attachment_ids
            del message_dict['attachments']
            del message_dict['cc']
            del message_dict['from']
            del message_dict['to']

            # message_create_from_mail_mail to avoid to notify message
            # (see mail.message.create)
            self.env['mail.message'].with_context(
                message_create_from_mail_mail=True).create(message_dict)
            _logger.info('Routing FatturaPA PEC E-Mail with Message-Id: {}'
                         .format(message.get('Message-Id')))
            return []

        elif self._context.get('fetchmail_server_id', False):
            fetchmail_server_id = self.env['fetchmail.server'].browse(
                self._context['fetchmail_server_id'])
            if fetchmail_server_id.is_fatturapa_pec:
                # todo send email for non-routable pec mail
                return []

        return super(MailThread, self).message_route(
            message, message_dict, model=model, thread_id=thread_id,
            custom_values=custom_values)
