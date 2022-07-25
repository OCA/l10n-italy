#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import (
    FatturapaCommon,
)
from odoo.tests import new_test_user


class TestBillNotification (FatturapaCommon):

    def setUp(self):
        super().setUp()
        self.notified_user = new_test_user(
            self.env,
            login='Notify E-bill',
        )
        self.sdicoop_channel = self.env.ref(
            'l10n_it_fatturapa_sdicoop.sdi_channel_sdicoop',
        )

    def test_e_bill_created_notify(self):
        """
        When an E-bill is received,
        the followers of the SdI channel are notified.
        """
        # Arrange: Set the channel in the company,
        # and a follower for the channel
        company = self.env.user.company_id
        notified_partner = self.notified_user.partner_id
        company.sdi_channel_id = self.sdicoop_channel
        company.sdi_channel_id.message_subscribe(
            partner_ids=notified_partner.ids,
        )
        # pre-condition: the partner is following the SdI channel
        self.assertIn(
            notified_partner,
            company.sdi_channel_id.message_partner_ids,
        )

        # Act: Receive the E-bill
        file_name = 'IT05979361218_001.xml'
        file_path, file_content = self.getFile(
            file_name,
            module_name='l10n_it_fatturapa_sdicoop',
        )
        attachment = company.sdi_channel_id.receive_fe(
            {
                file_name: file_content,
            },
            {},
        )

        # Assert: The SdI channel's follower is following the E-bill
        self.assertIn(
            notified_partner,
            attachment.message_partner_ids,
        )
        # There is a message of subtype E-bill received
        received_e_bill_subtype = self.env.ref(
            'l10n_it_sdi_channel.e_bill_received',
        )
        messages = attachment.message_ids
        received_e_bill_message = messages.filtered(
            lambda m: m.subtype_id == received_e_bill_subtype
        )
        self.assertEqual(len(received_e_bill_message), 1)
        # The message notifies the SdI channel's follower
        self.assertIn(
            notified_partner,
            received_e_bill_message.needaction_partner_ids,
        )
