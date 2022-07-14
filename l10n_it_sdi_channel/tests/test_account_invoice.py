#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestAccountInvoice(FatturaPACommon):
    def setUp(self):
        super().setUp()
        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        self.env.company.name = "YourCompany"
        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = True
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.state_id = self.env.ref("base.state_us_2").id
        self.env.company.partner_id.zip = "00100"
        self.env.company.partner_id.phone = "06543534343"
        self.env.company.email = "info@yourcompany.example.com"
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        validates the invoice and exports the attachment.
        """
        # Arrange: create a draft invoice with no attachment
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, "draft")
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
        self.assertIn("Expected singleton", exc_message)
        self.assertIn("sdi.channel", exc_message)
        self.assertEqual(invoice.state, "posted")
        self.assertTrue(invoice.fatturapa_attachment_out_id)

    def test_action_open_export_send_sdi_ui(self):
        """
        Check that the "Validate, export and send to SdI" button
        clicked in the UI (where an exception causes a ROLLBACK)
        does not validate the invoice or export the attachment.
        """
        # Arrange: create a draft invoice with no attachment
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, "draft")
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
        self.assertIn("Expected singleton", exc_message)
        self.assertIn("sdi.channel", exc_message)
        self.assertEqual(invoice.state, "draft")
        self.assertFalse(invoice.fatturapa_attachment_out_id)
