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

        self.sdi_coop_channel = self.env["sdi.channel"].create(
            [
                {
                    "name": "Test SdiCoop channel",
                    "channel_type": "sdi_coop",
                }
            ]
        )

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        tries to send the e-invoice.
        """
        # Arrange: set the SdI channel
        # and create a draft invoice with no attachment
        self.env.company.sdi_channel_id = self.sdi_coop_channel
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, "draft")
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act and Assert: open, export and send.
        # This raises an exception
        # because sending mechanism will be implemented by depending modules
        with self.assertRaises(NotImplementedError):
            invoice.action_open_export_send_sdi()
