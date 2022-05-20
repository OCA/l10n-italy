#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SdIChannel (models.Model):
    _inherit = 'sdi.channel'

    channel_type = fields.Selection(
        selection_add=[
            ("sdi_coop", "SDICoop (Web service)"),
        ],
    )

    def send_via_sdi_coop(self, attachment_out_ids):
        """Override this method to send the attachments to the web service."""
        raise NotImplementedError()
