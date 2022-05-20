#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class SendToSdI(models.TransientModel):
    _name = 'wizard.fatturapa.send_to_sdi'
    _description = "Wizard to send multiple e-invoice to SdI"

    @api.multi
    def send_to_sdi(self):
        if self.env.context.get('active_ids'):
            attachments = self.env['fatturapa.attachment.out'].browse(
                self.env.context['active_ids'])
            attachments.send_to_sdi()
