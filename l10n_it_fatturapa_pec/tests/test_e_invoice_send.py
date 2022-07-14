# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from .e_invoice_common import EInvoiceCommon
from odoo.tools import mute_logger


class TestEInvoiceSend(EInvoiceCommon):

    def setUp(self):
        super(TestEInvoiceSend, self).setUp()

    def test_send_check_fetchmail(self):
        """Sending e-invoice when there is no
        PEC server configured raises UserError"""
        e_invoice = self._create_e_invoice()

        # There is no PEC server configured
        with self.assertRaises(UserError):
            e_invoice.send_to_sdi()

    @mute_logger("odoo.addons.mail.models.mail_mail")
    def test_sender_error(self):
        """Sending e-invoice without configuring email_from_for_fatturaPA
        fails to send the email"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        self.env.user.company_id.sdi_channel_id. \
            pec_server_id.email_from_for_fatturaPA = False

        e_invoice.send_to_sdi()
        self.assertEqual(e_invoice.state, 'sender_error')

    def test_send(self):
        """Sending e-invoice changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_to_sdi()
        self.assertEqual(e_invoice.state, 'sent')

    def test_send_empty_file(self):
        """Sending e-invoice without file content must be blocked"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.datas = False
        with self.assertRaises(UserError):
            e_invoice.send_to_sdi()

    def test_wizard_send(self):
        """Sending e-invoice with wizard changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        wiz = self.env['wizard.fatturapa.send_to_sdi'].create({})
        wiz.with_context(active_ids=e_invoice.ids).send_to_sdi()
        self.assertEqual(e_invoice.state, 'sent')

    def test_resend_reset(self):
        """Re-sending e-invoice raises UserError"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_to_sdi()
        self.assertEqual(e_invoice.state, 'sent')

        # Cannot re-send e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.send_to_sdi()

        # Cannot reset e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.reset_to_ready()

    def test_resend_after_regenerate(self):
        """Re-sending e-invoice raises UserError"""
        invoice = self._create_invoice()
        invoice.action_invoice_open()

        wizard = self._get_export_wizard(invoice)
        action = wizard.exportFatturaPA()
        e_invoice = self.env[action['res_model']].browse(action['res_id'])

        self._create_fetchmail_pec_server()
        e_invoice.send_to_sdi()
        self.assertEqual(e_invoice.state, 'sent')

        # Set the e_invoice to error
        e_invoice.state = 'sender_error'

        wizard.with_context(active_id=invoice.id).\
            exportFatturaPARegenerate()
        self.assertEqual(e_invoice.state, "ready")

        with self.assertRaises(UserError):
            invoice.action_invoice_cancel()

        e_invoice.state = 'sender_error'
        invoice.journal_id.update_posted = True
        invoice.action_invoice_cancel()
        invoice.refresh()
        invoice.action_invoice_draft()
        invoice.refresh()
        invoice.action_invoice_open()
        invoice.refresh()

        action = wizard.with_context(active_id=invoice.id).\
            exportFatturaPARegenerate()

        e_invoice = self.env[action['res_model']].browse(action['res_id'])

        # set SDI address after first sending
        self.env.user.company_id.sdi_channel_id.email_exchange_system = (
            'sdi01@pec.fatturapa.it')
        # Send it again
        e_invoice.send_to_sdi()
        self.assertEqual(e_invoice.state, 'sent')

    def test_action_open_export_send_sdi(self):
        """
        Check that the "Validate, export and send to SdI" button
        sends the e-invoice.
        """
        # Arrange: create a draft invoice with no attachment
        invoice = self._create_invoice()
        self._create_fetchmail_pec_server()
        self.assertEqual(invoice.state, 'draft')
        self.assertFalse(invoice.fatturapa_attachment_out_id)

        # Act: open, export and send the invoice
        invoice.action_open_export_send_sdi()
        e_invoice = invoice.fatturapa_attachment_out_id

        self.assertEqual(e_invoice.state, 'sent')
