# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo import tests

from odoo.addons.l10n_it_fatturapa_fatturhello.tests.common import (
    MODULE,
    REQUEST_PATH,
    Common,
)


@tests.tagged("post_install", "-at_install")
class TestDownload(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cron = cls.env.ref(f"{MODULE}.ir_cron_fatturhello_import_e_bills")
        cls.cron.user_id.company_ids |= cls.env.company

    def _get_e_bills_capturer(self):
        return tests.RecordCapturer(self.env["fatturapa.attachment.in"], [])

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
        self._login(self.channel)
        company = self.env.company
        cron = self.cron
        # pre-condition
        self.assertIn(company, cron.user_id.company_ids)
        self.assertEqual(company.sdi_channel_id, self.channel)
        self.assertFalse(company.fatturhello_last_downloaded_e_bill_identifer)

        # Act
        with (
            mock.patch(REQUEST_PATH) as mock_request,
            self._get_e_bills_capturer() as e_bills_capturer,
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
        e_bills = e_bills_capturer.records
        e_bill = e_bills[0]
        self.assertEqual(e_bill.name, "IT01234567890_FPR03.xml")
        # The created E-Bill can be imported
        wizard = (
            self.env["wizard.import.fatturapa"]
            .with_context(
                active_ids=e_bill.ids,
                active_model=e_bill._name,
            )
            .create({})
        )
        with self._get_bills_capturer() as bills_capturer:
            wizard.importFatturaPA()
        bills = bills_capturer.records
        self.assertRecordValues(
            bills.sorted("ref"),
            [
                {
                    "ref": "123",
                },
                {
                    "ref": "456",
                },
            ],
        )
