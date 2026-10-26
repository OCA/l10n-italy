# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.modules import get_module_resource
from odoo.tests import tagged
from odoo.tools import mute_logger

from .e_invoice_common import EInvoiceCommon


class FakeIMAPServer:
    """Minimal IMAP server double recording the flags operations."""

    def __init__(self, messages):
        self.messages = messages
        self.store_calls = []
        self.selected = False
        self.closed = False
        self.logged_out = False

    def select(self, readonly=False):
        self.selected = True
        return "OK", [b"1"]

    def search(self, charset, criteria):
        numbers = [str(i).encode() for i in range(1, len(self.messages) + 1)]
        return "OK", [b" ".join(numbers)]

    def fetch(self, num, query):
        raw_message = self.messages[int(num) - 1]
        return "OK", [(b"1 (RFC822 {})", raw_message), b")"]

    def store(self, num, command, flags):
        self.store_calls.append((num, command, flags))
        return "OK", [b""]

    def close(self):
        self.closed = True

    def logout(self):
        self.logged_out = True


@tagged("post_install", "-at_install")
class TestPecFetchMail(EInvoiceCommon):
    def setUp(self):
        super().setUp()
        self.PEC_server = self._create_fetchmail_pec_server()
        self.attach_in_model = self.env["fatturapa.attachment.in"]

    @staticmethod
    def _get_file(filename):
        path = get_module_resource("l10n_it_fatturapa_pec", "tests", "data", filename)
        with open(path) as test_data:
            return test_data.read()

    def _get_imap_server(self, filename):
        imap_server = FakeIMAPServer([self._get_file(filename)])
        events = []

        original_store = imap_server.store

        def store(num, command, flags):
            events.append("store %s" % command)
            return original_store(num, command, flags)

        imap_server.store = store
        return imap_server, events

    def test_imap_message_seen_after_commit(self):
        """The message is marked as read only once it has been saved"""
        imap_server, events = self._get_imap_server(
            "POSTA CERTIFICATA_ Invio File 7339338.txt"
        )
        self.PEC_server.write({"server_type": "imap"})
        with mock.patch.object(
            type(self.PEC_server), "connect", return_value=imap_server
        ), mock.patch.object(
            self.env.cr, "commit", side_effect=lambda: events.append("commit")
        ):
            self.PEC_server.fetch_mail()

        self.assertEqual(events, ["store -FLAGS", "commit", "store +FLAGS"])
        self.assertTrue(
            self.attach_in_model.search(
                [("name", "=", "IT02652600210_00007.xml")], limit=1
            )
        )

    def test_imap_message_not_seen_if_commit_fails(self):
        """If the commit fails the message is not marked as read

        Otherwise it would never be fetched again, because only unseen
        messages are searched.
        """
        imap_server, _events = self._get_imap_server(
            "POSTA CERTIFICATA_ Invio File 7339338.txt"
        )
        self.PEC_server.write({"server_type": "imap"})
        with mock.patch.object(
            type(self.PEC_server), "connect", return_value=imap_server
        ), mock.patch.object(
            self.env.cr, "commit", side_effect=Exception("DB connection lost")
        ), mock.patch.object(
            type(self.PEC_server), "notify_or_log"
        ) as notify_or_log:
            self.PEC_server.fetch_mail()

        self.assertEqual(imap_server.store_calls, [(b"1", "-FLAGS", "\\Seen")])
        self.assertIn("DB connection lost", self.PEC_server.last_pec_error_message)
        self.assertTrue(notify_or_log.called)

    def test_pop_message_deleted_after_commit(self):
        """The message is deleted only once it has been saved"""
        events = []
        with mock.patch("odoo.addons.fetchmail.models.fetchmail.POP3") as mock_pop3:
            instance = mock_pop3.return_value
            instance.stat.return_value = (1, 1)
            instance.retr.return_value = (
                "",
                [self._get_file("POSTA CERTIFICATA_ Invio File 7339338.txt")],
                "",
            )
            instance.dele.side_effect = lambda num: events.append("dele")
            with mock.patch.object(
                self.env.cr, "commit", side_effect=lambda: events.append("commit")
            ):
                self.PEC_server.fetch_mail()

        self.assertEqual(events, ["commit", "dele"])
        self.assertIn(1, instance.dele.call_args_list[0][0])

    def test_pop_message_not_deleted_if_commit_fails(self):
        """If the commit fails the message is not deleted from the server"""
        with mock.patch("odoo.addons.fetchmail.models.fetchmail.POP3") as mock_pop3:
            instance = mock_pop3.return_value
            instance.stat.return_value = (1, 1)
            instance.retr.return_value = (
                "",
                [self._get_file("POSTA CERTIFICATA_ Invio File 7339338.txt")],
                "",
            )
            with mock.patch.object(
                self.env.cr, "commit", side_effect=Exception("DB connection lost")
            ), mock.patch.object(type(self.PEC_server), "notify_or_log"):
                self.PEC_server.fetch_mail()

        self.assertFalse(instance.dele.called)
        self.assertTrue(instance.quit.called)

    def test_failed_message_not_marked_seen(self):
        """A message that cannot be processed is not marked as read

        So that it is processed again at the next fetch.
        """
        imap_server, _events = self._get_imap_server(
            "POSTA CERTIFICATA_ Invio File 7339338 (broken XML).txt"
        )
        self.PEC_server.write({"server_type": "imap"})
        with mock.patch.object(
            type(self.PEC_server), "connect", return_value=imap_server
        ), mock.patch.object(type(self.PEC_server), "notify_or_log"), mute_logger(
            "odoo.addons.l10n_it_fatturapa_in.models.attachment",
            "odoo.addons.l10n_it_fatturapa_pec.models.fetchmail",
            "odoo.addons.l10n_it_sdi_channel.models.sdi",
        ):
            self.PEC_server.fetch_mail()

        self.assertEqual(imap_server.store_calls, [(b"1", "-FLAGS", "\\Seen")])
        self.assertTrue(self.PEC_server.last_pec_error_message)
