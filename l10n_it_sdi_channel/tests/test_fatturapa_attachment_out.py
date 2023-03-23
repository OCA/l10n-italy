#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_sdi_channel.models.fatturapa_attachment_out import (
    STATE_SUBTYPE_MAPPING,
)
from odoo.addons.mail.tests.common import MailCommon


class TestFatturaPAAttachmentOut(MailCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attachment_model = cls.env["fatturapa.attachment.out"]

    def test_track_subtype(self):
        """When the State of the Attachment is updated, a Message is sent."""
        # Arrange
        attachment = self.attachment_model.create(
            {
                "name": "Test Attachment",
            }
        )
        self.flush_tracking()
        creation_message = attachment.message_ids
        self.assertEqual(len(creation_message), 1)

        # Act
        new_state = "sent"
        attachment.state = new_state
        self.flush_tracking()

        # Assert
        state_update_message = attachment.message_ids - creation_message
        self.assertEqual(len(state_update_message), 1)
        subtype_xmlid = STATE_SUBTYPE_MAPPING.get(new_state)
        self.assertEqual(state_update_message.subtype_id, self.env.ref(subtype_xmlid))
