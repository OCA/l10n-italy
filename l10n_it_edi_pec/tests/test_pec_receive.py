# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import TestItEdiPecCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestPecReceive(TestItEdiPecCommon):
    def _process_pec_email(self, filename):
        """Process a PEC email from test data through message_process."""
        incoming_mail = self._get_test_file(filename)
        with patch.object(self.env.cr, "commit", lambda: None):
            self.env["mail.thread"].with_context(
                default_fetchmail_server_id=self.pec_fetch_server.id
            ).message_process(False, incoming_mail)

    def test_process_response_rc(self):
        """Receiving a 'Ricevuta di consegna' (RC) sets state to forwarded."""
        move = self._create_sent_invoice("IT03339130126_00009.xml")
        self._process_pec_email("POSTA CERTIFICATA_ Ricevuta di consegna 6782414.txt")
        self.assertEqual(move.l10n_it_edi_state, "forwarded")

    def test_process_response_mc(self):
        """Receiving 'Mancata consegna' (MC) sets state to forward_failed."""
        move = self._create_sent_invoice("IT14627831002_02621.xml")
        self._process_pec_email("POSTA CERTIFICATA_mancata_consegna.txt")
        self.assertEqual(move.l10n_it_edi_state, "forward_failed")

    def test_process_consegna(self):
        """Receiving a 'CONSEGNA' posts a message on the move."""
        move = self._create_sent_invoice("IT03339130126_00009.xml")
        messages_before = self.env["mail.message"].search_count(
            [("res_id", "=", move.id), ("model", "=", "account.move")]
        )
        self._process_pec_email("CONSEGNA_ IT03339130126_00009.xml.txt")
        messages_after = self.env["mail.message"].search_count(
            [("res_id", "=", move.id), ("model", "=", "account.move")]
        )
        self.assertGreater(messages_after, messages_before)

    def test_process_accettazione(self):
        """Receiving an 'ACCETTAZIONE' posts a message on the move."""
        move = self._create_sent_invoice("IT03339130126_00009.xml")
        messages_before = self.env["mail.message"].search_count(
            [("res_id", "=", move.id), ("model", "=", "account.move")]
        )
        self._process_pec_email("ACCETTAZIONE_ IT03339130126_00009.xml.txt")
        messages_after = self.env["mail.message"].search_count(
            [("res_id", "=", move.id), ("model", "=", "account.move")]
        )
        self.assertGreater(messages_after, messages_before)

    def test_process_incoming_invoice(self):
        """Receiving an incoming invoice creates a new account.move."""
        moves_before = self.env["account.move"].search([])
        self._process_pec_email("POSTA CERTIFICATA_ Invio File 7339338.txt")
        moves_after = self.env["account.move"].search([]) - moves_before
        self.assertTrue(moves_after)
        # Check that the attachment was created
        attachment = (
            self.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("res_id", "in", moves_after.ids),
                    ("res_model", "=", "account.move"),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ]
            )
        )
        self.assertTrue(attachment)

    def test_process_incoming_invoice_base64(self):
        """Receiving an incoming invoice with base64 attachment creates a new move."""
        moves_before = self.env["account.move"].search([])
        self._process_pec_email("POSTA CERTIFICATA_ Invio File 7339338 (base64).txt")
        moves_after = self.env["account.move"].search([]) - moves_before
        self.assertTrue(moves_after)
        attachment = (
            self.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("res_id", "in", moves_after.ids),
                    ("res_model", "=", "account.move"),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ]
            )
        )
        self.assertTrue(attachment)

    def test_process_incoming_invoice_duplicate(self):
        """Duplicate incoming invoice is skipped."""
        self._process_pec_email("POSTA CERTIFICATA_ Invio File 7339338.txt")
        moves_after_first = self.env["account.move"].search([])
        # Process same email again
        self._process_pec_email("POSTA CERTIFICATA_ Invio File 7339338.txt")
        moves_after_second = self.env["account.move"].search([])
        # No new move should be created
        self.assertEqual(len(moves_after_first), len(moves_after_second))

    def test_process_incoming_invoice_broken_xml(self):
        """Receiving a broken XML sends a notification to e_inv_notify_partner_ids."""
        incoming_mail = self._get_test_file(
            "POSTA CERTIFICATA_ Invio File 7339338 (broken XML).txt"
        )
        outbound_mail_model = self.env["mail.mail"]
        error_mail_domain = [
            (
                "recipient_ids",
                "in",
                self.pec_fetch_server.e_inv_notify_partner_ids.ids,
            ),
        ]
        error_mails_before = outbound_mail_model.search_count(error_mail_domain)

        with mock.patch("odoo.addons.mail.models.fetchmail.IMAP4_SSL") as mock_imap:
            instance = mock_imap.return_value
            instance.search.return_value = ("OK", [b"1"])
            instance.fetch.return_value = ("OK", [(b"1", incoming_mail)])
            instance.store.return_value = True

            with mute_logger(
                "odoo.addons.l10n_it_edi_pec.models.fetchmail_server",
            ):
                self.pec_fetch_server.fetch_mail(raise_exception=False)

        error_mails = outbound_mail_model.search(error_mail_domain)
        self.assertGreater(len(error_mails), error_mails_before)
        self.assertTrue(self.pec_fetch_server.last_pec_error_message)

    def test_unrelated_pec_email_raises(self):
        """PEC email not related to e-invoice raises UserError."""
        # Build a minimal email that is NOT from SdI and doesn't match
        # CONSEGNA/ACCETTAZIONE patterns
        raw_email = (
            b"From: someone@pec.example.it\r\n"
            b"To: test@pec.example.it\r\n"
            b"Subject: Some unrelated PEC message\r\n"
            b"Date: Mon, 1 Jan 2024 10:00:00 +0100\r\n"
            b"Message-Id: <test@example.it>\r\n"
            b"\r\n"
            b"Body text\r\n"
        )
        with self.assertRaises(UserError) as cm:
            self.env["mail.thread"].with_context(
                default_fetchmail_server_id=self.pec_fetch_server.id
            ).message_process(False, raw_email)
        self.assertIn("Some unrelated PEC message", str(cm.exception))
        self.assertIn("not processed", str(cm.exception))

    def test_fetchmail_error_count_and_reset(self):
        """PEC server auto-disables after max retry failures."""
        self.pec_fetch_server.pec_error_count = 5
        max_retry = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("fetchmail.pec.max.retry", default="5")
        )
        self.assertEqual(max_retry, 5)

        with mock.patch("odoo.addons.mail.models.fetchmail.IMAP4") as mock_imap:
            instance = mock_imap.return_value
            instance.select.side_effect = Exception("Connection failed")

            with mute_logger(
                "odoo.addons.l10n_it_edi_pec.models.fetchmail_server",
            ):
                self.pec_fetch_server.fetch_mail(raise_exception=False)

        # Error count exceeded max_retry -> server disabled
        self.assertEqual(self.pec_fetch_server.state, "draft")

    def test_notification_type_from_filename(self):
        """Test extraction of notification type from SDI filenames."""
        MailThread = self.env["mail.thread"]
        test_cases = [
            ("IT01234567890_12345_RC_001.xml", "RC"),
            ("IT01234567890_12345_NS_001.xml", "NS"),
            ("IT01234567890_12345_MC_001.xml", "MC"),
            ("IT01234567890_12345_NE_001.xml", "NE"),
            ("IT01234567890_12345_DT_001.xml", "DT"),
        ]
        for filename, expected_type in test_cases:
            result = MailThread._l10n_it_edi_sdi_get_type_from_filename(filename)
            self.assertEqual(
                result,
                expected_type,
                f"Failed for filename: {filename}",
            )

    def test_action_check_triggers_fetchmail(self):
        """action_check_l10n_it_edi triggers fetchmail for PEC companies."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        called_on = []

        def tracking_fetch_mail(self_inner, *args, **kwargs):
            called_on.append(self_inner)

        with mock.patch.object(
            type(self.pec_fetch_server), "fetch_mail", tracking_fetch_mail
        ):
            move.action_check_l10n_it_edi()
        self.assertEqual(len(called_on), 1)
        self.assertEqual(called_on[0], self.pec_fetch_server)
