#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import \
    FatturaPACommon


class TestAccountInvoice (FatturaPACommon):

    def setUp(self):
        super().setUp()
        self.sdi_coop_channel = self.env['sdi.channel'].create([{
            'name': "Test SdiCoop channel",
            'channel_type': 'sdi_coop',
        }])

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        tries to send the e-invoice.
        """
        # Arrange: set the SdI channel
        # and create a draft invoice with no attachment
        self.env.user.company_id.sdi_channel_id = self.sdi_coop_channel
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, 'draft')
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act and Assert: open, export and send.
        # This raises an exception
        # because sending mechanism will be implemented by depending modules
        with self.assertRaises(NotImplementedError):
            invoice.action_open_export_send_sdi()
