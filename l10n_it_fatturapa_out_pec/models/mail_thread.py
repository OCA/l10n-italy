# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
#
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or (at
#    your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/lgpl-3.0.txt.
#
##############################################################################

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None,
                      custom_values=None):
        if "@pec.fatturapa.it" in message.__getitem__('Reply-To'): # FIXME Unreliable?
            _logger.info("Processing FatturaPA PEC Response with Message-Id: {}"
                         .format(message.get('Message-Id')))
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

        return super(MailThread, self).message_route(message, message_dict,
            model=model, thread_id=thread_id, custom_values=custom_values)

