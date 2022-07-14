#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import \
    FatturaPACommon


class TestAccountInvoice (FatturaPACommon):

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        validates the invoice and exports the attachment.
        """
        # Arrange: create a draft invoice with no attachment
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, 'draft')
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act: open, export and send.
        # This raises an exception because there is no channel,
        # we can't create a channel yet
        # because channel types are defined by depending modules
        with self.assertRaises(ValueError) as ve:
            invoice.action_open_export_send_sdi()
        exc_message = ve.exception.args[0]

        # Assert: we are missing the SdI channel,
        # but invoice is validated and attachment has been created
        self.assertIn('Expected singleton', exc_message)
        self.assertIn('sdi.channel', exc_message)
        self.assertEqual(invoice.state, 'open')
        self.assertTrue(invoice.fatturapa_attachment_out_id)

    def test_action_open_export_send_sdi_ui(self):
        """
        Check that the "Validate, export and send to SdI" button
        clicked in the UI (where an exception causes a ROLLBACK)
        does not validate the invoice or export the attachment.
        """
        # Arrange: create a draft invoice with no attachment
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, 'draft')
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act: open, export and send.
        # This raises an exception because there is no channel,
        # we can't create a channel yet
        # because channel types are defined by depending modules
        with self.assertRaises(ValueError) as ve, self.env.cr.savepoint():
            invoice.action_open_export_send_sdi()
        exc_message = ve.exception.args[0]

        # Assert: we are missing the SdI channel,
        # but invoice is still in draft and attachment has not been created
        self.assertIn('Expected singleton', exc_message)
        self.assertIn('sdi.channel', exc_message)
        self.assertEqual(invoice.state, 'draft')
        self.assertFalse(invoice.fatturapa_attachment_out_id)
