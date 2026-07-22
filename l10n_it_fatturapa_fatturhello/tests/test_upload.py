# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from unittest import mock

from odoo import tests

from odoo.addons.l10n_it_fatturapa_fatturhello.tests.common import (
    MODULE,
    REQUEST_PATH,
    Common,
)
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


@tests.tagged("post_install", "-at_install")
class TestUpload(Common, FatturaPACommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.update(
            {
                "country_id": cls.env.ref("base.it").id,
                "state_id": cls.env.ref("base.state_it_rm").id,
                "street": "Via Roma",
                "city": "Roma",
                "zip": "00101",
                "fatturapa_fiscal_position_id": cls.env.ref(
                    "l10n_it_fatturapa.fatturapa_RF01"
                ).id,
            }
        )
        cls.cron = cls.env.ref(f"{MODULE}.ir_cron_fatturhello_update_e_invoices_status")
        cls.cron.user_id.company_ids |= cls.env.company

    def test_success(self):
        """An invoice can be uploaded."""
        # Arrange
        self._login(self.channel)
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.res_partner_fatturapa_0,
            amounts=[
                100,
            ],
        )
        # pre-condition
        self.assertEqual(invoice.state, "draft")
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_open_export_send_sdi()

        # Assert
        e_invoice = invoice.fatturapa_attachment_out_id
        self.assertEqual(e_invoice.state, "sent_to_fatturhello")
        self.assertEqual(invoice.fatturapa_state, "sent_to_fatturhello")
        self.assertEqual(e_invoice.fatturhello_protocol, "201701000021074")

    def test_status_update(self):
        """The status of uploaded e-invoices is updated
        based on Fatturhello status."""
        # Arrange
        cron = self.cron
        self._login(self.channel)
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.res_partner_fatturapa_0,
            amounts=[
                100,
            ],
        )
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_open_export_send_sdi()
        e_invoice = invoice.fatturapa_attachment_out_id
        # Change the file name to match the one in test's status updates
        e_invoice.name = "IT04075500373_EMZjW.xml"
        # pre-condition
        self.assertEqual(e_invoice.state, "sent_to_fatturhello")
        self.assertFalse(e_invoice.fatturhello_last_processed_status_datetime)

        # Act
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("status_success"),
            ]
            cron.method_direct_trigger()

        # Assert
        self.assertEqual(e_invoice.state, "validated")
        self.assertEqual(
            e_invoice.fatturhello_last_processed_status_datetime,
            datetime(2020, 7, 1, 14, 51),
        )

    def test_sent_to_fatturhello_unlink(self):
        """An e-invoice that has been sent to fatturhello can be deleted."""
        # Arrange
        self._login(self.channel)
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.res_partner_fatturapa_0,
            amounts=[
                100,
            ],
        )
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_open_export_send_sdi()
        e_invoice = invoice.fatturapa_attachment_out_id
        # pre-condition
        self.assertEqual(e_invoice.state, "sent_to_fatturhello")

        # Act
        e_invoice.unlink()

        # Assert
        self.assertFalse(e_invoice.exists())
