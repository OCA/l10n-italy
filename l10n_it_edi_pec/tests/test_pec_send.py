# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from unittest import mock

from odoo.tests import tagged

from odoo.addons.account_edi_proxy_client.models.account_edi_proxy_user import (
    AccountEdiProxyError,
)

from .common import TestItEdiPecCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestPecSend(TestItEdiPecCommon):
    def test_pec_upload(self):
        """Test that _l10n_it_edi_upload sends via PEC."""
        invoice = self._create_and_post_invoice()
        files = [
            {
                "filename": "IT01234560157_00001.xml",
                "xml": base64.b64encode(b"<xml/>").decode(),
                "destination_code": "0000000",
            }
        ]
        with mock.patch.object(
            type(self.env["ir.mail_server"]), "send_email"
        ) as mock_send:
            result = invoice._l10n_it_edi_upload(files)

        self.assertIn("IT01234560157_00001.xml", result)
        self.assertIn("id_transaction", result["IT01234560157_00001.xml"])
        self.assertTrue(
            result["IT01234560157_00001.xml"]["id_transaction"].startswith("pec_")
        )
        mock_send.assert_called_once()

    def test_pec_upload_fallback_to_standard(self):
        """When PEC is disabled, _l10n_it_edi_upload falls back to standard."""
        self.company.l10n_it_edi_use_pec = False
        invoice = self._create_and_post_invoice()
        files = [
            {
                "filename": "IT01234560157_00001.xml",
                "xml": base64.b64encode(b"<xml/>").decode(),
                "destination_code": "0000000",
            }
        ]
        # Standard upload would call proxy, which fails without
        # proxy configuration (edi_mode is not set)
        with mock.patch.object(
            type(self.env["ir.mail_server"]), "send_email"
        ) as mock_send:
            with self.assertRaises(KeyError):
                invoice._l10n_it_edi_upload(files)
        mock_send.assert_not_called()

    def test_pec_upload_error(self):
        """Test that send errors raise AccountEdiProxyError."""
        invoice = self._create_and_post_invoice()
        files = [
            {
                "filename": "IT01234560157_00001.xml",
                "xml": base64.b64encode(b"<xml/>").decode(),
                "destination_code": "0000000",
            }
        ]
        with mock.patch.object(
            type(self.env["ir.mail_server"]),
            "send_email",
            side_effect=Exception("SMTP error"),
        ):
            with self.assertRaises(AccountEdiProxyError):
                invoice._l10n_it_edi_upload(files)

    def test_pec_export_check_ok(self):
        """Company with full PEC config passes export check."""
        errors = self.company._l10n_it_edi_export_check()
        # No proxy user error
        self.assertNotIn("l10n_it_edi_settings_l10n_it_edi_proxy_user_id", errors)
        # No PEC errors
        self.assertNotIn("l10n_it_edi_pec_server", errors)
        self.assertNotIn("l10n_it_edi_pec_email_from", errors)
        self.assertNotIn("l10n_it_edi_pec_fetch_server", errors)
        self.assertNotIn("l10n_it_edi_pec_email_exchange_system", errors)

    def test_pec_export_check_missing_server(self):
        """Missing outgoing PEC server triggers error."""
        self.company.l10n_it_edi_pec_server_id = False
        errors = self.company._l10n_it_edi_export_check()
        self.assertIn("l10n_it_edi_pec_server", errors)

    def test_pec_export_check_missing_email_from(self):
        """Missing PEC sender email triggers error."""
        self.pec_smtp_server.l10n_it_edi_pec_email_from = False
        errors = self.company._l10n_it_edi_export_check()
        self.assertIn("l10n_it_edi_pec_email_from", errors)

    def test_pec_export_check_missing_fetch_server(self):
        """Missing incoming PEC server triggers error."""
        self.company.l10n_it_edi_pec_fetch_server_id = False
        errors = self.company._l10n_it_edi_export_check()
        self.assertIn("l10n_it_edi_pec_fetch_server", errors)

    def test_pec_export_check_fetch_server_not_confirmed(self):
        """Incoming PEC server not confirmed triggers error."""
        self.pec_fetch_server.state = "draft"
        errors = self.company._l10n_it_edi_export_check()
        self.assertIn("l10n_it_edi_pec_fetch_server_state", errors)

    def test_pec_export_check_missing_sdi_email(self):
        """Missing SDI PEC email triggers error."""
        self.company.l10n_it_edi_pec_email_exchange_system = False
        errors = self.company._l10n_it_edi_export_check()
        self.assertIn("l10n_it_edi_pec_email_exchange_system", errors)

    def test_pec_invoice_not_resendable(self):
        """An invoice already sent via PEC cannot be re-sent."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        self.assertEqual(move.l10n_it_edi_state, "processing")
        # Core guard: _l10n_it_edi_ready_for_xml_export returns False
        # when l10n_it_edi_state is not False/rejected
        self.assertFalse(move._l10n_it_edi_ready_for_xml_export())

    def test_find_mail_server_excludes_pec(self):
        """PEC server must not be selected for regular emails."""
        # _find_mail_server is used by connect() and mail.mail._send()
        # to automatically pick an SMTP server. PEC servers must be excluded.
        mail_server, _email_from = self.env["ir.mail_server"]._find_mail_server(
            "user@example.com"
        )
        if mail_server:
            self.assertFalse(
                mail_server.is_l10n_it_edi_pec,
                "PEC server should not be selected for regular emails",
            )

    def test_update_send_state_skips_pec(self):
        """_l10n_it_edi_update_send_state should skip PEC moves."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        # Should not raise (PEC moves are silently skipped)
        move._l10n_it_edi_update_send_state()
        # State should remain unchanged
        self.assertEqual(move.l10n_it_edi_state, "processing")
