#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import (
    FatturapaCommon,
)
from odoo.tests import new_test_user, SavepointCase


class TestBillNotification (FatturapaCommon, SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.notified_user = new_test_user(
            cls.env,
            login='Notify E-bill',
        )
        cls.not_notified_user = new_test_user(
            cls.env,
            login='Do not Notify E-bill',
        )
        cls.sdicoop_channel = cls.env.ref(
            'l10n_it_fatturapa_sdicoop.sdi_channel_sdicoop',
        )
        cls.channel_received_e_bill = \
            cls.env.ref('l10n_it_sdi_channel.sdi_channel_e_bill_received')
        cls.attachment_received_e_bill = \
            cls.env.ref('l10n_it_sdi_channel.e_bill_received')

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
        messages = attachment.message_ids
        received_e_bill_message = messages.filtered(
            lambda m: m.subtype_id == self.attachment_received_e_bill
        )
        self.assertEqual(len(received_e_bill_message), 1)
        # The message notifies the SdI channel's follower
        self.assertIn(
            notified_partner,
            received_e_bill_message.needaction_partner_ids,
        )

    def test_e_bill_created_no_notify(self):
        """
        When an E-bill is received,
        the channel followers that do not have the 'E-bill received' subtype
        are not notified.
        """
        # Arrange: Set the channel in the company,
        # and a follower for the channel
        company = self.env.user.company_id
        not_notified_partner = self.not_notified_user.partner_id
        company.sdi_channel_id = self.sdicoop_channel
        all_subtypes, internal_subtypes, external_subtypes = \
            self.env['mail.message.subtype'].default_subtypes(
                self.sdicoop_channel._name,
            )
        self.sdicoop_channel.message_subscribe(
            partner_ids=not_notified_partner.ids,
            subtype_ids=(all_subtypes - self.channel_received_e_bill).ids,
        )
        # pre-condition: the Partner is following the SdI Channel,
        # but not the E-bill Received Subtype
        self.assertIn(
            not_notified_partner,
            company.sdi_channel_id.message_partner_ids,
        )
        received_e_bill_followers = self.sdicoop_channel.message_follower_ids \
            .filtered(
                lambda f: self.channel_received_e_bill in f.subtype_ids
            ) \
            .mapped('partner_id')
        self.assertNotIn(
            not_notified_partner,
            received_e_bill_followers,
        )

        # Act: Receive the E-bill
        file_name = 'IT05979361218_001.xml'
        file_path, file_content = self.getFile(
            file_name,
            module_name='l10n_it_fatturapa_sdicoop',
        )
        attachment = self.sdicoop_channel.receive_fe(
            {
                file_name: file_content,
            },
            {},
        )

        # Assert: There is a message of subtype E-bill received,
        # but the partner is not following it
        messages = attachment.message_ids
        received_e_bill_message = messages.filtered(
            lambda m: m.subtype_id == self.attachment_received_e_bill
        )
        self.assertEqual(len(received_e_bill_message), 1)
        # The message notifies the SdI channel's follower
        self.assertNotIn(
            not_notified_partner,
            received_e_bill_message.needaction_partner_ids,
        )
