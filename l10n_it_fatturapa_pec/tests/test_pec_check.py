# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import email
from datetime import date, datetime
from email.message import EmailMessage
from unittest import mock

from odoo.exceptions import UserError
from odoo.modules import get_module_resource
from odoo.tests import tagged

from .e_invoice_common import EInvoiceCommon


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


@tagged("post_install", "-at_install")
class TestPecCheck(EInvoiceCommon):
    def setUp(self):
        super().setUp()
        self.PEC_server = self._create_fetchmail_pec_server()
        self.sdi_channel = self.env.ref("l10n_it_fatturapa_pec.sdi_channel_pec")
        self.sdi_channel.fetch_pec_server_id = self.PEC_server
        self.attach_in_model = self.env["fatturapa.attachment.in"]
        self.raw_mail = self._get_file("POSTA CERTIFICATA_ Invio File 7339338.txt")
        self.e_invoice_name = "IT02652600210_00007.xml"

    @staticmethod
    def _get_file(filename):
        path = get_module_resource("l10n_it_fatturapa_pec", "tests", "data", filename)
        with open(path, "rb") as test_data:
            return test_data.read()

    def _process_mail(self):
        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, self.raw_mail)

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
        self.assertTrue(
            self.attach_in_model.search([("name", "=", self.e_invoice_name)], limit=1)
        )

        found = self._check()
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["is_einvoice_xml_found"])

    def test_check_mailbox_is_source(self):
        """The check starts from the mailbox, not from Odoo attachments."""
        self.attach_in_model.create({"name": "IT01234567890_99999.xml"})

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

        found = self.PEC_server._check_pec_message(direct_xml_mail, self.env.company)
        self.assertEqual(len(found), 1)
        self.assertFalse(found[0]["is_einvoice_xml_found"])

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, direct_xml_mail)
        self.assertTrue(
            self.attach_in_model.search([("name", "=", self.e_invoice_name)], limit=1)
        )

        found = self.PEC_server._check_pec_message(direct_xml_mail, self.env.company)
        self.assertTrue(found[0]["is_einvoice_xml_found"])

    def test_check_multiple_attachments(self):
        """Find the invoice among multiple attachments."""
        found = self.PEC_server._check_pec_message(
            self._get_multi_attachment_mail(), self.env.company
        )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["file_name"], "IT01234567890_12345.xml")
        self.assertFalse(found[0]["is_einvoice_xml_found"])

    def test_check_uses_server_company(self):
        """Only attachments of the server company are considered."""
        self.attach_in_model.create({"name": self.e_invoice_name})
        other_company = self.env["res.company"].sudo().create({"name": "Other company"})

        found = self.PEC_server._check_pec_message(self.raw_mail, self.env.company)
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["is_einvoice_xml_found"])
        found = self.PEC_server._check_pec_message(self.raw_mail, other_company)
        self.assertEqual(len(found), 1)
        self.assertFalse(found[0]["is_einvoice_xml_found"])

    def test_check_not_pec_server(self):
        """The check cannot run on a server that is not a PEC server."""
        self.PEC_server.is_fatturapa_pec = False

        with self.assertRaises(UserError):
            self.PEC_server.check_received_e_invoices(
                "2018-12-01 00:00:00", "2018-12-31 23:59:59"
            )

    def test_check_ignores_response(self):
        """SdI responses without an e-invoice are ignored."""
        response_mail = self._get_file("ACCETTAZIONE_ IT03339130126_00009.xml.txt")

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
