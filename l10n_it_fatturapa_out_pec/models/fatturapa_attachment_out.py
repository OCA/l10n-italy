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

from odoo import api, fields, models


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    state = fields.Selection([('ready', 'Ready to Send'),
                              ('sent', 'Sent'),
                              ('validated', 'Validated'),
                              ('sender_error', 'Sender Error'),
                              ('recipient_error', 'Recipient Error')],
                             string="State",
                             default="ready",)

    def get_pec_mail_server(self):
        # TODO Should we pick a PEC SMTP server dedicated to fatturaPA only?
        return self.env['ir.mail_server'].search([('is_pec', '=', True)],
                                                 limit=1)

    @api.multi
    def send_via_pec(self):
        pec_mail_server = self.get_pec_mail_server()

        mail_message = self.env['mail.message'].create({
            'model': self._name,
            'res_id': self.id,
            'subject': self.name,
            'body': "XML file for FatturaPA {} sent to Exchange System to the"
                    " email address {}."
                .format(self.name, pec_mail_server.email_exchange_system),
            'attachment_ids': [(6, 0, [self.ir_attachment_id.id])],
            'email_from': pec_mail_server.email_from_for_fatturaPA,
            'mail_server_id': pec_mail_server.id
        })

        self.env['mail.mail'].create({
            'mail_message_id': mail_message.id,
            'body_html': mail_message.body,
            'email_to': pec_mail_server.email_exchange_system,
        }).send()  # TODO Should we disable some mail.* config params before
                   # TODO sending? See: https://tinyurl.com/ybr45fxd

        self.state = 'sent'
