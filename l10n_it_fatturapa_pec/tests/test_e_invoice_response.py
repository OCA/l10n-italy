# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_pec.tests.e_invoice_common \
    import EInvoiceCommon
from odoo.modules import get_module_resource


class TestEInvoiceResponse(EInvoiceCommon):

    def setUp(self):
        super(TestEInvoiceResponse, self).setUp()
        self.PEC_server = self._create_fetchmail_pec_server()
        self.env.user.company_id.vat = 'IT03339130126'
        self.set_sequences(9, 15, '2018-01-07')
        self.attach_in_model = self.env['fatturapa.attachment.in']

    @staticmethod
    def _get_file(filename):
        path = get_module_resource(
            'l10n_it_fatturapa_pec', 'tests', 'data', filename)
        with open(path) as test_data:
            return test_data.read()

    def test_process_response_RC(self):
        """Receiving a 'Ricevuta di consegna' sets the state of the
        e-invoice to 'validated'"""
        e_invoice = self._create_e_invoice()
        e_invoice.send_via_pec()

        incoming_mail = self._get_file(
            'POSTA CERTIFICATA_ Ricevuta di consegna 6782414.txt')

        self.env['mail.thread'] \
            .with_context(fetchmail_server_id=self.PEC_server.id) \
            .message_process(False, incoming_mail)
        self.assertEqual(e_invoice.state, 'validated')

    def test_process_response_CONSEGNA(self):
        """Receiving a 'CONSEGNA' posts a mail.message in the e-invoice"""
        e_invoice = self._create_e_invoice()
        e_invoice.send_via_pec()

        incoming_mail = self._get_file(
            'CONSEGNA_ IT03339130126_00009.xml.txt')

        messages_nbr = self.env['mail.message'].search_count([
            ('model', '=', e_invoice._name),
            ('res_id', '=', e_invoice.id)])

        self.env['mail.thread'] \
            .with_context(fetchmail_server_id=self.PEC_server.id) \
            .message_process(False, incoming_mail)

        messages_nbr = self.env['mail.message'].search_count([
            ('model', '=', e_invoice._name),
            ('res_id', '=', e_invoice.id)]) - messages_nbr

        self.assertTrue(messages_nbr)

    def test_process_response_ACCETTAZIONE(self):
        """Receiving a 'ACCETTAZIONE' posts a mail.message in the e-invoice"""
        e_invoice = self._create_e_invoice()
        e_invoice.send_via_pec()

        incoming_mail = self._get_file(
            'ACCETTAZIONE_ IT03339130126_00009.xml.txt')

        messages_nbr = self.env['mail.message'].search_count([
            ('model', '=', e_invoice._name),
            ('res_id', '=', e_invoice.id)])

        self.env['mail.thread'] \
            .with_context(fetchmail_server_id=self.PEC_server.id) \
            .message_process(False, incoming_mail)

        messages_nbr = self.env['mail.message'].search_count([
            ('model', '=', e_invoice._name),
            ('res_id', '=', e_invoice.id)]) - messages_nbr

        self.assertTrue(messages_nbr)

    def test_process_response_INVO(self):
        """Receiving a 'Invio File' creates a new e-invoice"""
        incoming_mail = self._get_file(
            'POSTA CERTIFICATA: Invio File 7339338.txt')

        e_invoices = self.attach_in_model.search([])

        self.env['mail.thread'] \
            .with_context(fetchmail_server_id=self.PEC_server.id) \
            .message_process(False, incoming_mail)

        e_invoices = self.attach_in_model.search([]) - e_invoices

        self.assertTrue(e_invoices)
        self.assertEqual(e_invoices.xml_supplier_id.vat,
                         'IT02652600210')
