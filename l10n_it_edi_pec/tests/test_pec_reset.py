# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.message import EmailMessage
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TestItEdiPecCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestPecReset(TestItEdiPecCommon):
    def _add_pdf(self, move):
        return self.env["ir.attachment"].create(
            {
                "name": "invoice.pdf",
                "raw": b"%PDF-1.4",
                "type": "binary",
                "res_model": "account.move",
                "res_id": move.id,
                "res_field": "invoice_pdf_report_file",
                "company_id": self.company.id,
            }
        )

    def _process_notification(self, attachment_name, nome_file):
        message = EmailMessage()
        message["From"] = '"Per conto di: sdi01@pec.fatturapa.it" <posta@pec.it>'
        message["Reply-To"] = "sdi01@pec.fatturapa.it"
        message["To"] = "test@pec.example.it"
        message["Subject"] = "POSTA CERTIFICATA: Notifica"
        message["Message-Id"] = f"<{attachment_name}@pec.fatturapa.it>"
        message.set_content("Notifica")
        message.add_attachment(
            f"<Notifica><NomeFile>{nome_file}</NomeFile></Notifica>".encode(),
            maintype="application",
            subtype="xml",
            filename=attachment_name,
        )
        with patch.object(self.env.cr, "commit", lambda: None):
            self.env["mail.thread"].with_context(
                default_fetchmail_server_id=self.pec_fetch_server.id
            ).message_process(False, message.as_bytes())

    def test_reset_keeps_files_as_history(self):
        """Reset clears the SDI state and keeps XML and PDF in the chatter."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        xml = move.l10n_it_edi_attachment_id
        pdf = self._add_pdf(move)
        move.invalidate_recordset()
        self.assertFalse(move._l10n_it_edi_ready_for_xml_export())

        move.action_l10n_it_edi_pec_reset()

        self.assertFalse(move.l10n_it_edi_state)
        self.assertFalse(move.l10n_it_edi_transaction)
        self.assertFalse(move.l10n_it_edi_attachment_id)
        self.assertFalse(move.invoice_pdf_report_id)
        self.assertTrue(move._l10n_it_edi_ready_for_xml_export())
        self.assertNotIn(
            "l10n_it_edi_pdf_already_generated",
            move._l10n_it_edi_base_export_check(),
        )
        for attachment, name in (
            (xml, "IT01234560157_00001.xml"),
            (pdf, "invoice.pdf"),
        ):
            self.assertTrue(attachment.exists())
            self.assertRegex(attachment.name, rf"^old_\d{{8}}-\d{{4}}_{name}$")
            self.assertFalse(attachment.res_field)
            self.assertEqual(attachment.res_id, move.id)
        message = move.message_ids[0]
        self.assertEqual(message.attachment_ids, xml | pdf)
        self.assertIn("IT01234560157_00001.xml", message.body)

    def test_reset_requires_processing(self):
        """Only a move waiting for an SDI answer can be reset."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        move.l10n_it_edi_state = "forwarded"
        with self.assertRaises(UserError):
            move.action_l10n_it_edi_pec_reset()

    def test_late_notification_after_reset(self):
        """A notification about a file kept as history still finds its move."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        move.action_l10n_it_edi_pec_reset()
        found = self.env["mail.thread"]._l10n_it_edi_sdi_find_move_by_attachment_name(
            "IT01234560157_00001.xml", company=self.company
        )
        self.assertEqual(found, move)
        # Underscores of the file name are not wildcards
        self.assertFalse(
            self.env["mail.thread"]._l10n_it_edi_sdi_find_move_by_attachment_name(
                "IT01234560157X00001.xml", company=self.company
            )
        )

    def test_notification_without_move_raises(self):
        """A notification whose e-invoice is not found is not dropped."""
        with self.assertRaises(UserError) as cm:
            self._process_notification(
                "IT01234560157_00009_RC_001.xml", "IT01234560157_00009.xml"
            )
        self.assertIn("IT01234560157_00009_RC_001.xml", str(cm.exception))

    def test_notification_unknown_type_raises(self):
        """A notification type that is not handled is not dropped."""
        move = self._create_sent_invoice("IT01234560157_00001.xml")
        with self.assertRaises(UserError) as cm:
            self._process_notification(
                "IT01234560157_00001_AT_001.xml", "IT01234560157_00001.xml"
            )
        self.assertIn("AT", str(cm.exception))
        self.assertEqual(move.l10n_it_edi_state, "processing")
