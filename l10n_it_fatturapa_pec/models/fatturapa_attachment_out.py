# Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018-2019 Lorenzo Battistini <https://github.com/eLBati>

import logging
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

RESPONSE_MAIL_REGEX = '[A-Z]{2}[a-zA-Z0-9]{11,16}_[a-zA-Z0-9]{,5}_[A-Z]{2}_' \
                      '[a-zA-Z0-9]{,3}'


class FatturaPAAttachmentOut(models.Model):
    _inherit = 'fatturapa.attachment.out'

    sending_user = fields.Many2one("res.users", "Sending User", readonly=True)

    @api.multi
    def parse_pec_response(self, message_dict):
        message_dict['model'] = self._name
        message_dict['res_id'] = 0

        regex = re.compile(RESPONSE_MAIL_REGEX)
        notifications = [x for x in message_dict['attachments']
                         if regex.match(x.fname)]

        if not notifications:
            raise UserError(_(
                "PEC message \"%s\" is coming from SDI but attachments do not "
                "match SDI response format. Please check."
            ) % (
                message_dict['subject']
            ))

        sdi_channel_model = self.env['sdi.channel']
        attachments = sdi_channel_model.receive_notification(
            {
                notification.fname: notification.content
                for notification in notifications
            },
        )

        # Link the message to the last attachment updated
        message_dict['res_id'] = attachments[-1].id
        return message_dict
