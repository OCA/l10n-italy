#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

STATE_SUBTYPE_MAPPING = {
    'ready': 'l10n_it_sdi_channel.e_invoice_ready',
    'sent': 'l10n_it_sdi_channel.e_invoice_sent',
    'sender_error': 'l10n_it_sdi_channel.e_invoice_sender_error',
    'recipient_error': 'l10n_it_sdi_channel.e_invoice_recipient_error',
    'rejected': 'l10n_it_sdi_channel.e_invoice_rejected',
    'validated': 'l10n_it_sdi_channel.e_invoice_validated',
    'accepted': 'l10n_it_sdi_channel.e_invoice_accepted',
}
"""
Map each state of fatturapa.attachment.out to
the mail.message.subtype that should be used to notify the user.
"""


class FatturaPAAttachmentOut (models.Model):
    _inherit = 'fatturapa.attachment.out'

    last_sdi_response = fields.Text(
        string='Last Response from Exchange System',
        default='No response yet',
        readonly=True,
    )

    @api.multi
    def send_to_sdi(self):
        states = self.mapped('state')
        if set(states) != {'ready'}:
            raise UserError(
                _("You can only send files in 'Ready to Send' state.")
            )

        company = self.env.user.company_id
        sdi_channel = company.sdi_channel_id
        send_result = sdi_channel.send(self)
        return send_result

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values:
            state_subtype = STATE_SUBTYPE_MAPPING.get(self.state)
            if state_subtype:
                return state_subtype
        return super()._track_subtype(init_values)
