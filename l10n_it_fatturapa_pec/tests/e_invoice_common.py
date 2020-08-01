# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common \
    import FatturaPACommon


class EInvoiceCommon(FatturaPACommon):

    def setUp(self):
        super(EInvoiceCommon, self).setUp()
        self.account_model = self.env['account.account']
        self.invoice_model = self.env['account.invoice']
        self.wizard_model = self.env['wizard.export.fatturapa']

        self.account_receivable_id = self.account_model.create(dict(
            code="REC",
            name="Receivable",
            user_type_id=self.ref('account.data_account_type_receivable'),
            reconcile=True,
        ))
        self.account_income_id = self.account_model.create(dict(
            code="INC",
            name="Income",
            user_type_id=self.ref('account.data_account_type_revenue'),
            reconcile=True,
        ))
        self.partner = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_2')
        self.product = self.env.ref('product.product_product_5')
        self.env.user.company_id.sdi_channel_id = self.env.ref(
            'l10n_it_sdi_channel.sdi_channel_pec')
        self.env.user.company_id.sdi_channel_id.pec_server_id = \
            self.env['ir.mail_server'].create({
                'name': 'dummy',
                'smtp_host': 'smtp_host',
                'email_from_for_fatturaPA': 'dummy@fatturapa.it'})

    def _create_invoice(self):
        invoice_line_data = {
            'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 1,
            'account_id': self.account_income_id.id,
            'name': self.product.name,
            'invoice_line_tax_ids': [
                (6, 0, [self.ref('l10n_it_fatturapa.tax_22')])]
        }
        return self.invoice_model.create(
            dict(
                name='Test Invoice',
                account_id=self.account_receivable_id.id,
                invoice_line_ids=[(0, 0, invoice_line_data)],
                partner_id=self.partner.id
            ))

    def _get_export_wizard(self, invoice):
        wizard = self.wizard_model.create({})
        return wizard.with_context(
            {'active_ids': [invoice.id]})

    def _create_e_invoice(self):
        invoice = self._create_invoice()
        invoice.action_invoice_open()

        wizard = self._get_export_wizard(invoice)
        action = wizard.exportFatturaPA()

        return self.env[action['res_model']].browse(action['res_id'])

    def _create_fetchmail_pec_server(self):
        return self.env['fetchmail.server'].create({
            'name': 'Test PEC server',
            'type': 'pop',
            'is_fatturapa_pec': True,
            'server': 'dummy',
            'port': 110,
            'user': 'dummy',
            'password': 'secret',
            'state': 'done',
            'e_inv_notify_partner_ids': [
                (6, 0, [self.env.ref("base.user_admin").partner_id.id])],
        })
