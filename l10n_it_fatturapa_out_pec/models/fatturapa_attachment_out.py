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

    @api.multi
    def send_via_pec(self):
        # TODO Do the actual sending of PEC
        self.state = 'sent'
