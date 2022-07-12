
import base64
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon)


class TestInvoiceWT(FatturaPACommon):

    def setUp(self):
        super(TestInvoiceWT, self).setUp()
        type_payable = self.env.ref('account.data_account_type_payable')
        type_receivable = self.env.ref('account.data_account_type_receivable')
        self.tax_0 = self.env.ref('l10n_it_fatturapa.tax_00_enas')
        self.wt_account_payable = self.env['account.account'].create({
            'name': 'Debiti per ritenute da versare',
            'code': 'WT_001',
            'user_type_id': type_payable.id,
            'reconcile': True,
        })
        self.wt_account_receivable = self.env['account.account'].create({
            'name': 'Crediti per ritenute subite',
            'code': 'WT_002',
            'user_type_id': type_receivable.id,
            'reconcile': True,
        })
        self.journal_misc = self.env['account.journal'].search(
            [('type', '=', 'general')])[0]
        vals_payment = {
            'name': "",
            'line_ids': [(0, 0, {'value': 'balance', 'days': 15})]
            }
        self.payment_term_15 = self.env['account.payment.term'].create(
            vals_payment)
        wt_vals = {
            'name': 'Code 1040',
            'code': '1040',
            'certification': True,
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'journal_id': self.journal_misc.id,
            'payment_term': self.payment_term_15.id,
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.a').id,
            'rate_ids': [(0, 0, {
                'tax': 20,
                'base': 1,
            })]
        }
        self.wt1040 = self.env['withholding.tax'].create(wt_vals)
        wt_vals = {
            'name': 'Enasarco',
            'code': 'Enasarco',
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'journal_id': self.journal_misc.id,
            'wt_types': 'enasarco',
            'payment_term': self.payment_term_15.id,
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.a').id,
            'rate_ids': [(0, 0, {
                'tax': 8.25,
                'base': 1,
            })]
            }
        self.enasarco = self.env['withholding.tax'].create(wt_vals)
        wt_vals = {
            'name': 'INPS',
            'code': 'INPS',
            'account_receivable_id': self.wt_account_receivable.id,
            'account_payable_id': self.wt_account_payable.id,
            'journal_id': self.journal_misc.id,
            'wt_types': 'inps',
            'payment_term': self.payment_term_15.id,
            'causale_pagamento_id': self.env.ref(
                'l10n_it_causali_pagamento.a').id,
            'rate_ids': [(0, 0, {
                'tax': 5.25,
                'base': 1,
            })]
            }
        self.inps = self.env['withholding.tax'].create(wt_vals)

    def test_e_invoice_wt(self):
        self.set_sequences(13, '2019-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [self.wt1040.id])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00011.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00011.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_enas_0(self):
        self.set_sequences(14, '2019-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.enasarco.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00014.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00014.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_enas_1(self):
        """
        Fill DatiCassaPrevidenziale with Enasarco data
        """
        self.set_sequences(15, '2019-01-07')
        self.enasarco.use_daticassaprev = True
        self.enasarco.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.enasarco.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00015.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00015.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_enas_2(self):
        """
        Fill DatiCassaPrevidenziale with Enasarco data,
        when DatiRiepilogo already has 0 VAT
        """
        self.set_sequences(16, '2019-01-07')
        self.enasarco.use_daticassaprev = True
        self.enasarco.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_0.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.enasarco.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00016.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00016.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_inps_0(self):
        self.set_sequences(17, '2019-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.inps.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00017.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00017.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_inps_1(self):
        """
        Fill DatiCassaPrevidenziale with INPS data
        """
        self.set_sequences(18, '2019-01-07')
        self.inps.use_daticassaprev = True
        self.inps.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_22.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.inps.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00018.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00018.xml',
            module_name='l10n_it_fatturapa_out_wt')

    def test_e_invoice_wt_inps_2(self):
        """
        Fill DatiCassaPrevidenziale with INPS data,
        when DatiRiepilogo already has 0 VAT
        """
        self.set_sequences(19, '2019-01-07')
        self.inps.use_daticassaprev = True
        self.inps.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create({
            'date_invoice': '2019-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'name': 'Service',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, [self.tax_0.id])],
                    'invoice_line_tax_wt_ids': [(6, 0, [
                        self.wt1040.id,
                        self.inps.id,
                    ])]
                }),
            ],
        })
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00019.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content, 'IT06363391001_00019.xml',
            module_name='l10n_it_fatturapa_out_wt')
