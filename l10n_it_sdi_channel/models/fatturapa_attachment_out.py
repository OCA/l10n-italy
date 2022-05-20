#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    def send_to_sdi(self):
        states = self.mapped("state")
        if set(states) != {"ready"}:
            raise UserError(_("You can only send files in 'Ready to Send' state."))

        company = self.env.company
        sdi_channel = company.sdi_channel_id
        send_result = sdi_channel.send(self)
        return send_result
