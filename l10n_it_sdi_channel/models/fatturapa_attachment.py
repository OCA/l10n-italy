#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FatturaPAAttachment (models.AbstractModel):
    _inherit = 'fatturapa.attachment'

    channel_id = fields.Many2one(
        comodel_name='sdi.channel',
        related="company_id.sdi_channel_id",
        store=True,
    )

    def _message_auto_subscribe_followers(
            self, updated_values, default_subtype_ids):
        res = super()._message_auto_subscribe_followers(
            updated_values, default_subtype_ids)
        updated_channel_id = updated_values.get('channel_id')
        if not updated_channel_id:
            # SdI channel is not explicitly set, so SdI channel's followers
            # won't be subscribed to current attachments.
            # Attachments might have the SdI channel set anyway
            # because it is a related field.
            # Add the SdI channel's followers
            # but only if all the attachments share the same SdI channel
            channel = self.mapped('channel_id')
            if all(attachment.channel_id == channel for attachment in self):
                subtype_model = self.env['mail.message.subtype']
                child_ids, def_ids, all_int_ids, parent, relation = \
                    subtype_model._get_auto_subscription_subtypes(self._name)
                for channel_follower in channel.message_follower_ids:
                    for channel_subtype in channel_follower.subtype_ids:
                        attachment_subtype_id = parent.get(channel_subtype.id)
                        if attachment_subtype_id:
                            res.append((
                                channel_follower.partner_id.id,
                                [attachment_subtype_id],
                                False,
                            ))
        return res
