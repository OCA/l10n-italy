# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo import tests

from odoo.addons.l10n_it_edi_fatturhello.tests.common import (
    REQUEST_PATH,
    Common,
)


@tests.tagged("post_install", "-at_install")
class TestDownload(Common):
    def _get_bills_capturer(self):
        return tests.RecordCapturer(
            self.env["account.move"],
            [
                ("move_type", "=", "in_invoice"),
            ],
        )

    def test_success(self):
        """E-Bills can be downloaded."""
        # Arrange
        company = self.company
        self._login(company)
        cron = self.cron
        # pre-condition
        self.assertIn(company, cron.user_id.company_ids)
        self.assertFalse(company.fatturhello_last_downloaded_e_bill_identifer)

        # Act
        with (
            mock.patch(REQUEST_PATH) as mock_request,
            self._get_bills_capturer() as bills_capturer,
        ):
            mock_request.side_effect = [
                self._get_response("login_success"),
                self._get_response("download_years_list_success"),
                self._get_response("download_list_success"),
                self._get_response("download_list_empty_success"),
                self._get_response(
                    "download_file_content_success",
                    headers_name="download_file_headers_success",
                ),
                self._get_response(
                    "download_file_content_success",
                    headers_name="download_file_headers_success",
                ),
            ]
            cron.method_direct_trigger()

        # Assert
        self.assertEqual(
            company.fatturhello_last_downloaded_e_bill_identifer,
            "201801000121236",
        )
        bills = bills_capturer.records
        self.assertEqual(
            bills.l10n_it_edi_attachment_id.name, "IT01234567890_FPR03.xml"
        )
        self.assertRecordValues(
            bills.sorted("ref"),
            [
                {
                    "ref": "123",
                },
            ],
        )
