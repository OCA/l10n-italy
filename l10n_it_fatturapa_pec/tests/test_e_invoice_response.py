# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import email

import mock

from odoo.fields import Datetime
from odoo.modules import get_module_resource
from odoo.tests import tagged
from odoo.tools import mute_logger, pycompat

from .e_invoice_common import EInvoiceCommon


@tagged("post_install", "-at_install")
class TestEInvoiceResponse(EInvoiceCommon):
    def setUp(self):
        super(TestEInvoiceResponse, self).setUp()
        self.PEC_server = self._create_fetchmail_pec_server()
        self.env.company.vat = "IT03339130126"
        self.set_sequences(15, "2018-01-07")
        self.attach_in_model = self.env["fatturapa.attachment.in"]

    @staticmethod
    def _get_file(filename):
        path = get_module_resource("l10n_it_fatturapa_pec", "tests", "data", filename)
        with open(path) as test_data:
            return test_data.read()

    def test_process_response_RC(self):
        """Receiving a 'Ricevuta di consegna' sets the state of the
        e-invoice to 'validated'"""
        e_invoice = self._create_e_invoice()
        self.set_e_invoice_file_id(e_invoice, "IT03339130126_00009.xml")
        e_invoice.send_via_pec()

        incoming_mail = self._get_file(
            "POSTA CERTIFICATA_ Ricevuta di consegna 6782414.txt"
        )

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, incoming_mail)
        self.assertEqual(e_invoice.state, "validated")

    def test_process_response_CONSEGNA(self):
        """Receiving a 'CONSEGNA' posts a mail.message in the e-invoice"""
        e_invoice = self._create_e_invoice()
        self.set_e_invoice_file_id(e_invoice, "IT03339130126_00009.xml")
        e_invoice.send_via_pec()

        incoming_mail = self._get_file("CONSEGNA_ IT03339130126_00009.xml.txt")

        messages_nbr = self.env["mail.message"].search_count(
            [("model", "=", e_invoice._name), ("res_id", "=", e_invoice.id)]
        )

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, incoming_mail)

        messages_nbr = (
            self.env["mail.message"].search_count(
                [("model", "=", e_invoice._name), ("res_id", "=", e_invoice.id)]
            )
            - messages_nbr
        )

        self.assertTrue(messages_nbr)

    def test_process_response_ACCETTAZIONE(self):
        """Receiving a 'ACCETTAZIONE' posts a mail.message in the e-invoice"""
        e_invoice = self._create_e_invoice()
        self.set_e_invoice_file_id(e_invoice, "IT03339130126_00009.xml")
        e_invoice.send_via_pec()

        incoming_mail = self._get_file("ACCETTAZIONE_ IT03339130126_00009.xml.txt")

        messages_nbr = self.env["mail.message"].search_count(
            [("model", "=", e_invoice._name), ("res_id", "=", e_invoice.id)]
        )

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, incoming_mail)

        messages_nbr = (
            self.env["mail.message"].search_count(
                [("model", "=", e_invoice._name), ("res_id", "=", e_invoice.id)]
            )
            - messages_nbr
        )

        self.assertTrue(messages_nbr)

    def test_process_response_INVIO(self):
        """Receiving a 'Invio File' creates a new e-invoice"""
        incoming_mail = self._get_file("POSTA CERTIFICATA_ Invio File 7339338.txt")

        e_invoices = self.attach_in_model.search([])

        msg_dict = self.env["mail.thread"].message_parse(
            self.from_string(incoming_mail)
        )

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, incoming_mail)

        e_invoices = self.attach_in_model.search([]) - e_invoices

        self.assertTrue(e_invoices)
        self.assertEqual(
            Datetime.from_string(e_invoices.e_invoice_received_date),
            Datetime.from_string(msg_dict["date"]),
        )
        self.assertEqual(e_invoices.xml_supplier_id.vat, "IT02652600210")

    def test_process_response_INVIO_broken_XML(self):
        """Receiving a 'Invio File' with a broken XML sends an email
        to e_inv_notify_partner_ids"""
        incoming_mail = self._get_file(
            "POSTA CERTIFICATA_ Invio File 7339338 (broken XML).txt"
        )
        xml_error = (
            "Namespace prefix ns1 on Fattura is not defined, "
            "line 1, column 13 (<string>, line 1)"
        )
        outbound_mail_model = self.env["mail.mail"]
        error_mail_domain = [
            ("body_html", "like", xml_error),
            ("recipient_ids", "in", self.PEC_server.e_inv_notify_partner_ids.ids),
        ]
        error_mails_nbr = outbound_mail_model.search_count(error_mail_domain)
        self.assertFalse(error_mails_nbr)

        with mock.patch("odoo.addons.fetchmail.models.fetchmail.POP3") as mock_pop3:
            instance = mock_pop3.return_value
            instance.stat.return_value = (1, 1)
            instance.retr.return_value = ("", [incoming_mail], "")

            with mute_logger("odoo.addons.l10n_it_fatturapa_pec.models.fetchmail"):
                self.PEC_server.fetch_mail()

        error_mails = outbound_mail_model.search(error_mail_domain)
        self.assertEqual(len(error_mails), 1)
        self.assertIn(xml_error, error_mails.body_html)
        self.assertIn(xml_error, self.PEC_server.last_pec_error_message)

    def test_process_response_MC(self):
        """Receiving a 'Mancata consegna' sets the state of the
        e-invoice to 'recipient_error'"""
        self.env.company.vat = "IT14627831002"
        self.set_sequences(2621, "2019-01-08")
        e_invoice = self._create_e_invoice()
        self.set_e_invoice_file_id(e_invoice, "IT14627831002_02621.xml")
        e_invoice.send_via_pec()

        incoming_mail = self._get_file("POSTA CERTIFICATA_mancata_consegna.txt")

        self.env["mail.thread"].with_context(
            fetchmail_server_id=self.PEC_server.id
        ).message_process(False, incoming_mail)
        self.assertEqual(e_invoice.state, "recipient_error")

    def from_string(self, text):
        return email.message_from_string(
            pycompat.to_text(text), policy=email.policy.SMTP
        )
