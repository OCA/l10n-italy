# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .e_invoice_common import EInvoiceCommon


@tagged("post_install", "-at_install")
class TestEInvoiceSend(EInvoiceCommon):
    def setUp(self):
        super(TestEInvoiceSend, self).setUp()

    def test_send_check_fetchmail(self):
        """Sending e-invoice when there is no
        PEC server configured raises UserError"""
        e_invoice = self._create_e_invoice()

        # There is no PEC server configured
        with self.assertRaises(UserError):
            e_invoice.send_via_pec()

    @mute_logger("odoo.addons.mail.models.mail_mail")
    def test_sender_error(self):
        """Sending e-invoice without configuring email_from_for_fatturaPA
        fails to send the email"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        self.env.company.sdi_channel_id.pec_server_id.email_from_for_fatturaPA = False

        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, "sender_error")

    def test_send(self):
        """Sending e-invoice changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, "sent")

    def test_send_empty_file(self):
        """Sending e-invoice without file content must be blocked"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.datas = False
        with self.assertRaises(UserError):
            e_invoice.send_via_pec()

    def test_wizard_send(self):
        """Sending e-invoice with wizard changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        wiz = self.env["wizard.fatturapa.send.pec"].create({})
        wiz.with_context(active_ids=e_invoice.ids).send_pec()
        self.assertEqual(e_invoice.state, "sent")

    def test_resend_reset(self):
        """Re-sending e-invoice raises UserError"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, "sent")

        # Cannot re-send e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.send_via_pec()

        # Cannot reset e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.reset_to_ready()

    def test_resend_after_regenerate(self):
        """Re-sending e-invoice raises UserError"""
        invoice = self._create_invoice()
        invoice.action_post()

        wizard = self._get_export_wizard(invoice)
        action = wizard.exportFatturaPA()
        e_invoice = self.env[action["res_model"]].browse(action["res_id"])

        self._create_fetchmail_pec_server()
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, "sent")

        # Set the e_invoice to error
        e_invoice.state = "sender_error"

        wizard.with_context(active_id=invoice.id).exportFatturaPARegenerate()
        self.assertEqual(e_invoice.state, "ready")

        e_invoice.state = "sender_error"
        invoice.button_draft()
        invoice.action_post()

        action = wizard.with_context(active_id=invoice.id).exportFatturaPARegenerate()

        e_invoice = self.env[action["res_model"]].browse(action["res_id"])

        # set SDI address after first sending
        self.env.company.sdi_channel_id.email_exchange_system = "sdi01@pec.fatturapa.it"
        # Send it again
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, "sent")
