# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from unittest import mock

from odoo import tests

from odoo.addons.l10n_it_edi_fatturhello.tests.common import (
    REQUEST_PATH,
    Common,
)


@tests.tagged("post_install", "-at_install")
class TestUpload(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company.update(
            {
                "fatturhello_is_used": True,
                "l10n_it_codice_fiscale": "06363391001",
                "vat": "06363391001",
            }
        )
        cls.cron.user_id.company_ids |= cls.company

    def test_success(self):
        """An invoice can be uploaded."""
        # Arrange
        self._login(self.company)
        invoice = self.init_invoice(
            "out_invoice",
            company=self.company,
            partner=self.italian_partner_a,
            amounts=[
                100,
            ],
            taxes=self.default_tax,
            post=True,
        )
        # pre-condition
        self.assertEqual(invoice.state, "posted")
        self.assertFalse(invoice.l10n_it_edi_state)

        # Act
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_l10n_it_edi_send()

        # Assert
        self.assertEqual(invoice.l10n_it_edi_state, "sent_to_fatturhello")
        self.assertEqual(invoice.fatturhello_protocol, "201701000021074")

    def test_status_update(self):
        """The status of uploaded e-invoices is updated
        based on Fatturhello status."""
        # Arrange
        cron = self.cron
        self._login(self.company)
        invoice = self.init_invoice(
            "out_invoice",
            company=self.company,
            partner=self.italian_partner_a,
            amounts=[
                100,
            ],
            taxes=self.default_tax,
            post=True,
        )
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_l10n_it_edi_send()
        e_invoice = invoice.l10n_it_edi_attachment_id
        # Change the file name to match the one in test's status updates
        e_invoice.name = "IT04075500373_EMZjW.xml"

        def mock_commit():
            pass

        # pre-condition
        self.assertEqual(invoice.l10n_it_edi_state, "sent_to_fatturhello")
        self.assertFalse(invoice.fatturhello_last_processed_status_datetime)

        # Act
        with (
            mock.patch(REQUEST_PATH) as mock_request,
            mock.patch.object(self.env.cr, "commit", mock_commit),
        ):
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("download_years_list_empty_success"),
                self._get_response("login_success"),
                self._get_response("status_success"),
            ]
            cron.method_direct_trigger()

        # Assert
        self.assertEqual(invoice.l10n_it_edi_state, "forwarded")
        self.assertEqual(
            invoice.fatturhello_last_processed_status_datetime,
            datetime(2020, 7, 1, 14, 51),
        )

    def test_sent_to_fatturhello_unlink(self):
        """An e-invoice that has been sent to fatturhello can be deleted."""
        # Arrange
        self._login(self.company)
        invoice = self.init_invoice(
            "out_invoice",
            company=self.company,
            partner=self.italian_partner_a,
            amounts=[
                100,
            ],
            taxes=self.default_tax,
            post=True,
        )
        with mock.patch(REQUEST_PATH) as mock_request:
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("upload_success"),
            ]
            invoice.action_l10n_it_edi_send()
        e_invoice = invoice.l10n_it_edi_attachment_id
        # pre-condition
        self.assertEqual(invoice.l10n_it_edi_state, "sent_to_fatturhello")

        # Act
        e_invoice.unlink()

        # Assert
        self.assertFalse(e_invoice.exists())
