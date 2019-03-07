# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.l10n_it_fatturapa_out.tests.fatturapa_common \
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
            user_type=self.ref('account.data_account_type_receivable'),
            reconcile=True,
        ))
        self.account_income_id = self.account_model.create(dict(
            code="INC",
            name="Income",
            user_type=self.ref('account.data_account_type_income'),
            reconcile=True,
        ))
        self.partner = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_2')
        self.product = self.env.ref('product.product_product_5')

    def _create_e_invoice(self):
        invoice_line_data = {
            'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 1,
            'account_id': self.account_income_id.id,
            'name': self.product.name,
            'invoice_line_tax_id': [
                (6, 0, [self.ref('l10n_it_fatturapa.tax_22')])]
        }
        recent_date = self.invoice_model.search(
            [('date_invoice', '!=', False)], order='date_invoice desc',
            limit=1).date_invoice
        invoice = self.invoice_model.create(
            dict(
                name='Test Invoice',
                date_invoice=recent_date,
                account_id=self.account_receivable_id.id,
                invoice_line=[(0, 0, invoice_line_data)],
                partner_id=self.partner.id
            ))
        invoice.signal_workflow('invoice_open')

        wizard = self.wizard_model.create({})
        action = wizard.with_context(
            {'active_ids': [invoice.id]}).exportFatturaPA()

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
            'state': 'done'
        })
