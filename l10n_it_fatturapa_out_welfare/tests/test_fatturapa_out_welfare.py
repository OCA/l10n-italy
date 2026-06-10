#  Copyright 2022 Simone Rubino - TAKOBI
#  Copyright 2025 Alex Comba - Agile Business Group
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.exceptions import UserError

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon,
)


class TestFatturaPAOUTWelfare(FatturaPACommon):
    def _get_welfare_amount(self, welfare, amount):
        """
        Return a Welfare Amount of type `welfare` and amount `amount`.
        """
        welfare_amount_model = self.env['welfare.fund.type.amount']
        welfare_amount = welfare_amount_model.create({
            'welfare_fund_type_id': welfare.id,
            'amount': amount,
        })
        return welfare_amount

    def _get_payable_account(self):
        """
        Return an account of Type Payable.
        """
        account_model = self.env['account.account']
        payable_account = account_model.create({
            'name': "Withholding Credit",
            'code': "WTPAY",
            'user_type_id': self.env.ref('account.data_account_type_payable').id,
            'reconcile': True,
        })
        return payable_account

    def _get_withholding_tax(self, payable_account, receivable_account):
        """
        Return a 20% Withholding Tax.
        """
        withholding_tax_model = self.env['withholding.tax']
        rate_vals = [{
            'tax': 20,
            'base': 1,
        }]
        withholding_tax = withholding_tax_model.create({
            'name': "Test WT",
            'code': "TWT",
            'account_receivable_id': receivable_account.id,
            'account_payable_id': payable_account.id,
            'journal_id': self.journal_misc.id,
            'causale_pagamento_id': self.env.ref('l10n_it_causali_pagamento.a').id,
            'payment_term': self.env.ref('account.account_payment_term_immediate').id,
            'rate_ids': [(0, 0, rate) for rate in rate_vals],
        })
        return withholding_tax

    def _get_invoice(self):
        """
        Return an invoice having 3 lines:
        - subtotal 100,
        - subtotal 100, with 10% Welfare and 20% Withholding Tax
        - subtotal 100, with 10% Welfare and 20% on another Welfare
        """
        # Cancel other open invoices to avoid conflict on date or sequence
        open_invoices = self.invoice_model.search([
            ('state', '=', 'open'),
        ])
        journals = open_invoices.mapped('journal_id')
        journals.update({'update_posted': True})
        open_invoices.action_cancel()

        date_invoice = '2023-01-01'
        self.set_sequences(1, date_invoice)
        invoice_vals = {
            'date_invoice': date_invoice,
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Cabinet with Doors',
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 100,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'welfare_fund_type_amount_ids': [(5, 0, 0)],
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'uom_id': self.product_uom_unit.id,
                    'name': 'Cabinet with Doors',
                    'price_unit': 100,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'welfare_fund_type_amount_ids': [(6, 0, [self.welfare_amount_INPS_10.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [self.withholding_tax.id])],
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'uom_id': self.product_uom_unit.id,
                    'name': 'Cabinet with Doors',
                    'price_unit': 100,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'welfare_fund_type_amount_ids': [(6, 0, [self.welfare_amount_ENPAM_20.id, self.welfare_amount_INPS_10.id])],
                }),
            ],
        }
        invoice = self.invoice_model.create(invoice_vals)
        invoice._onchange_invoice_line_wt_ids()
        return invoice

    def setUp(self):
        super(TestFatturaPAOUTWelfare, self).setUp()
        self.journal_misc = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        self.welfare_amount_INPS_10 = self._get_welfare_amount(
            self.env.ref('l10n_it_fatturapa.21'),
            10,
        )
        self.welfare_amount_ENPAM_20 = self._get_welfare_amount(
            self.env.ref('l10n_it_fatturapa.8'),
            20,
        )
        self.withholding_tax = self._get_withholding_tax(
            self._get_payable_account(),
            self.a_recv,
        )

    def test_export_welfare_withholding(self):
        """
        Check that an invoice having Welfare Amounts and Withholding Taxes
        is correctly converted to an Electronic Invoice.
        """
        invoice = self._get_invoice()
        # Check that Welfare Lines have to be generated
        # before validating the invoice
        with self.assertRaises(UserError) as ue:
            invoice.action_invoice_open()
        exc_message = ue.exception.args[0]
        self.assertIn('regenerate Welfare Lines', exc_message)
        self.assertIn(invoice.display_name, exc_message)
        # Export the Electronic Invoice
        invoice.button_regenerate_welfare_lines()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_random.xml')
        xml_content = attachment.datas.decode('base64')
        self.check_content(
            xml_content,
            'IT06363391001_random.xml',
            module_name='l10n_it_fatturapa_out_welfare',
        )
