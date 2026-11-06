# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import email
import io
import zipfile
from collections import namedtuple
from datetime import date, datetime
from email.message import EmailMessage
from unittest import mock

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TestItEdiPecCommon

Attachment = namedtuple("Attachment", "fname content info")


class FakeIMAPServer:
    def __init__(self, messages):
        self.messages = messages
        self.search_args = None
        self.selected_readonly = False
        self.closed = False
        self.logged_out = False

    def select(self, readonly=False):
        self.selected_readonly = readonly
        return "OK", [b"1"]

    def search(self, charset, criteria):
        self.search_args = (charset, criteria)
        numbers = [str(i).encode() for i in range(1, len(self.messages) + 1)]
        return "OK", [b" ".join(numbers)]

    def fetch(self, num, query):
        raw_message = self.messages[int(num) - 1]
        return "OK", [(b"1 (BODY[] {})", raw_message), b")"]

    def close(self):
        self.closed = True

    def logout(self):
        self.logged_out = True


@tagged("post_install_l10n", "post_install", "-at_install")
class TestPecCheck(TestItEdiPecCommon):
    def setUp(self):
        super().setUp()
        self.PEC_server = self.pec_fetch_server
        self.company.l10n_it_edi_pec_email_exchange_system = "sdi03@pec.fatturapa.it"
        self.raw_mail = self._get_test_file("POSTA CERTIFICATA_ Invio File 7339338.txt")
        self.e_invoice_name = "IT02652600210_00007.xml"

    def _process_mail(self):
        self.env["mail.thread"].with_context(
            default_fetchmail_server_id=self.PEC_server.id
        ).message_process(False, self.raw_mail)

    def _get_invoice_attachment(self, file_name=None, company=None):
        return (
            self.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("name", "=", file_name or self.e_invoice_name),
                    ("company_id", "=", (company or self.company).id),
                    ("res_model", "=", "account.move"),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ],
                limit=1,
            )
        )

    def _create_imported_attachment(self, file_name, company=None):
        company = company or self.company
        move = (
            self.env["account.move"]
            .with_company(company)
            .create({"move_type": "in_invoice"})
        )
        return (
            self.env["ir.attachment"]
            .sudo()
            .with_company(company)
            .create(
                {
                    "name": file_name,
                    "raw": b"<xml/>",
                    "type": "binary",
                    "res_model": "account.move",
                    "res_id": move.id,
                    "res_field": "l10n_it_edi_attachment_file",
                    "company_id": company.id,
                }
            )
        )

    def _check(self):
        with mock.patch.object(
            type(self.PEC_server),
            "_get_pec_messages",
            return_value=[self.raw_mail],
        ):
            return self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )

    def _get_direct_xml_mail(self):
        original_mail = email.message_from_bytes(
            self.raw_mail, policy=email.policy.SMTP
        )
        invoice_content = False
        for part in original_mail.walk():
            if part.get_filename() == self.e_invoice_name:
                invoice_content = part.get_content()
                break
        message = EmailMessage()
        message["From"] = "sdi03@pec.fatturapa.it"
        message["To"] = "recipient@pec.example.com"
        message["Subject"] = "POSTA CERTIFICATA: Invio File 7339338"
        message["Message-Id"] = "<direct-xml@pec.example.com>"
        message["Date"] = "Sat, 8 Dec 2018 12:26:18 +0100"
        message.set_content("Direct XML invoice")
        message.add_attachment(
            invoice_content,
            maintype="application",
            subtype="xml",
            filename=self.e_invoice_name,
        )
        return message.as_bytes()

    def _get_multi_attachment_mail(self):
        """Return a multi-attachment message from sdi05."""
        original_mail = email.message_from_bytes(
            self.raw_mail, policy=email.policy.SMTP
        )
        invoice_content = False
        for part in original_mail.walk():
            if part.get_filename() == self.e_invoice_name:
                invoice_content = part.get_content()
                break
        message = EmailMessage()
        message["From"] = (
            '"Per conto di: sdi05@pec.fatturapa.it" ' "<posta-certificata@legalmail.it>"
        )
        message["Reply-To"] = "sdi05@pec.fatturapa.it"
        message["Return-Path"] = "<sdi05@pec.fatturapa.it>"
        message["To"] = "recipient@pec.example.com"
        message["Subject"] = "POSTA CERTIFICATA: Invio File 17673588393"
        message["Message-Id"] = "<multi-attachment@pec.example.com>"
        message["Date"] = "Thu, 2 Jul 2026 00:12:57 +0200"
        message.set_content("Certified email")
        message.add_attachment(
            b"not an invoice",
            maintype="application",
            subtype="pdf",
            filename="invoice.pdf",
        )
        message.add_attachment(
            invoice_content,
            maintype="application",
            subtype="xml",
            filename="IT01234567890_12345.xml",
        )
        return message.as_bytes()

    def test_check_missing_e_invoice(self):
        """An e-invoice received but not imported is reported as missing."""
        found = self._check()

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["file_name"], self.e_invoice_name)
        self.assertFalse(found[0]["is_einvoice_xml_found"])
        self.assertEqual(
            found[0]["message_id"],
            "<opec288.20181208122618.17535.2665.1.3@pcert.sogei.it>",
        )

    def test_check_imported_e_invoice(self):
        """An e-invoice imported from PEC is reported as found."""
        self._process_mail()
        self.assertTrue(self._get_invoice_attachment())

        found = self._check()
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["is_einvoice_xml_found"])

    def test_check_mailbox_is_source(self):
        """The check starts from the mailbox, not from Odoo attachments."""
        self._create_imported_attachment("IT01234567890_99999.xml")

        found = self._check()
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["file_name"], self.e_invoice_name)
        self.assertFalse(found[0]["is_einvoice_xml_found"])

        with mock.patch.object(
            type(self.PEC_server), "_get_pec_messages", return_value=[]
        ):
            found = self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )
        self.assertFalse(found)

    def test_direct_xml_invoice(self):
        """Invoices delivered directly as XML are checked and imported."""
        direct_xml_mail = self._get_direct_xml_mail()
        sdi_email = self.company.l10n_it_edi_pec_email_exchange_system

        found = self.PEC_server._check_pec_message(
            direct_xml_mail, sdi_email, self.company
        )
        self.assertEqual(len(found), 1)
        self.assertFalse(found[0]["is_einvoice_xml_found"])

        self.env["mail.thread"].with_context(
            default_fetchmail_server_id=self.PEC_server.id
        ).message_process(False, direct_xml_mail)
        self.assertTrue(self._get_invoice_attachment())

        found = self.PEC_server._check_pec_message(
            direct_xml_mail, sdi_email, self.company
        )
        self.assertTrue(found[0]["is_einvoice_xml_found"])

    def test_check_multiple_attachments_and_other_sdi_address(self):
        """Accept any sdiNN address and find the invoice among attachments."""
        found = self.PEC_server._check_pec_message(
            self._get_multi_attachment_mail(),
            "sdi03@pec.fatturapa.it",
            self.company,
        )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["file_name"], "IT01234567890_12345.xml")
        self.assertFalse(found[0]["is_einvoice_xml_found"])

    def test_check_uses_server_company(self):
        """Only attachments of the server company are considered."""
        self._create_imported_attachment(self.e_invoice_name)
        other_company = self.company_data["company"]
        sdi_email = self.company.l10n_it_edi_pec_email_exchange_system

        found = self.PEC_server._check_pec_message(
            self.raw_mail, sdi_email, self.company
        )
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["is_einvoice_xml_found"])
        found = self.PEC_server._check_pec_message(
            self.raw_mail, sdi_email, other_company
        )
        self.assertEqual(len(found), 1)
        self.assertFalse(found[0]["is_einvoice_xml_found"])

    def test_check_not_pec_server(self):
        """The check cannot run on a server that is not a PEC server."""
        self.PEC_server.is_l10n_it_edi_pec = False

        with self.assertRaises(UserError):
            self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )

    def test_check_missing_sdi_email(self):
        """The SdI email address must be configured on the company."""
        self.company.l10n_it_edi_pec_email_exchange_system = False

        with self.assertRaises(UserError):
            self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )

    def test_check_other_sdi_email(self):
        """Messages not coming from the configured SdI address are ignored."""
        self.company.l10n_it_edi_pec_email_exchange_system = "other@pec.fatturapa.it"

        self.assertFalse(self._check())

    def test_check_ignores_response(self):
        """SdI responses without an e-invoice are ignored."""
        self.company.l10n_it_edi_pec_email_exchange_system = (
            "posta-certificata@pec.aruba.it"
        )
        response_mail = self._get_test_file(
            "ACCETTAZIONE_ IT03339130126_00009.xml.txt"
        )

        with mock.patch.object(
            type(self.PEC_server),
            "_get_pec_messages",
            return_value=[response_mail],
        ):
            missing = self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )

        self.assertFalse(missing)

    def test_check_dates(self):
        """The check validates the selected period."""
        with self.assertRaises(UserError):
            self.PEC_server.check_received_e_invoices(
                "2018-12-31 23:59:59", "2018-12-01 00:00:00"
            )
        with self.assertRaises(UserError):
            self.PEC_server.check_received_e_invoices(False, "2018-12-01 00:00:00")

    def test_get_e_invoice_file_names_zip(self):
        """E-invoices inside a ZIP archive are checked one by one."""
        content = io.BytesIO()
        with zipfile.ZipFile(content, "w") as zip_file:
            zip_file.writestr(self.e_invoice_name, b"<xml/>")
            zip_file.writestr("not-an-invoice.txt", b"text")
        attachment = Attachment("invoices.zip", content.getvalue(), {})

        file_names = self.PEC_server._get_e_invoice_file_names(attachment)

        self.assertEqual(file_names, [self.e_invoice_name])

    def test_get_pec_messages_imap(self):
        """Only messages in the period are retrieved from IMAP."""
        imap_server = FakeIMAPServer([self.raw_mail])
        with mock.patch.object(
            type(self.PEC_server), "connect", return_value=imap_server
        ):
            messages = self.PEC_server._get_pec_messages_imap(
                datetime(2018, 12, 1), datetime(2018, 12, 31, 23, 59, 59)
            )

        self.assertEqual(messages, [self.raw_mail])
        self.assertIn('SINCE "01-Dec-2018"', imap_server.search_args[1])
        self.assertIn('BEFORE "01-Jan-2019"', imap_server.search_args[1])
        self.assertTrue(imap_server.selected_readonly)
        self.assertTrue(imap_server.closed)
        self.assertTrue(imap_server.logged_out)

    def test_get_pec_messages_imap_datetime_filter(self):
        """The selected datetimes are used to filter retrieved messages."""
        imap_server = FakeIMAPServer([self.raw_mail])
        with mock.patch.object(
            type(self.PEC_server), "connect", return_value=imap_server
        ):
            messages = self.PEC_server._get_pec_messages_imap(
                datetime(2018, 12, 8, 12, 0, 0),
                datetime(2018, 12, 8, 23, 59, 59),
            )

        # The message date is 12:26:18 +0100, i.e. 11:26:18 UTC
        self.assertFalse(messages)

    def test_get_pec_messages_connection_failure(self):
        """A disabled or failed connection raises a clear error."""
        with mock.patch.object(type(self.PEC_server), "connect", return_value=False):
            with self.assertRaises(UserError):
                self.PEC_server._get_pec_messages(
                    datetime(2018, 12, 1), datetime(2018, 12, 31, 23, 59, 59)
                )

    def test_format_imap_date(self):
        self.assertEqual(
            self.PEC_server._format_imap_date(date(2018, 12, 1)),
            "01-Dec-2018",
        )
