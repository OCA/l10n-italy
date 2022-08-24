# -*- coding: utf-8 -*-

import base64
import tempfile
from openerp.modules import get_module_resource
from openerp.tests.common import SingleTransactionCase


class FatturapaCommon(SingleTransactionCase):

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_in'
        path = get_module_resource(module_name, 'tests', 'data', filename)
        with open(path, 'rb') as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def create_wt(self):
        return self.env['withholding.tax'].create({
            'name': '1040',
            'code': '1040',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 20.0})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.a').id,
        })

    def create_wt_23_20(self):
        return self.env['withholding.tax'].create({
            'name': '2320',
            'code': '2320',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 23.0, 'base': 0.2})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.a').id,
        })

    def create_wt_23_50(self):
        return self.env['withholding.tax'].create({
            'name': '2320',
            'code': '2320',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 23.0, 'base': 0.5})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.a').id,
        })

    def create_wt_26_20q(self):
        return self.env['withholding.tax'].create({
            'name': '2620q',
            'code': '2620q',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 26.0, 'base': 0.2})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.q').id,
        })

    def create_wt_26_40q(self):
        return self.env['withholding.tax'].create({
            'name': '2640q',
            'code': '2640q',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 26.0, 'base': 0.4})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.q').id,
        })

    def create_wt_27_20q(self):
        return self.env['withholding.tax'].create({
            'name': '2720q',
            'code': '2720q',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'wt_types': 'ritenuta',
            'rate_ids': [(0, 0, {'tax': 27.0, 'base': 0.2})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.q').id,
        })

    def create_wt_4q(self):
        return self.env['withholding.tax'].create({
            'name': '4q',
            'code': '4q',
            'wt_types': 'enasarco',
            'account_receivable_id': self.payable_account_id,
            'account_payable_id': self.payable_account_id,
            'journal_id': self.env['account.journal'].search(
                [('type', '=', 'general')], limit=1).id,
            'payment_term': self.env.ref('account.account_payment_term').id,
            'rate_ids': [(0, 0, {'tax': 4.0, 'base': 1.0})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.q').id,
        })

    def create_res_bank(self):
        return self.env['res.bank'].create({
            'name': 'Banca generica',
            'bic': 'BCITITMM',
        })

    def create_fiscal_years(self):
        self.fiscalyear2019 = self.account_fiscalyear_model.create(
            vals={
                'name': '2019',
                'code': '2019',
                'date_start': '2019-01-01',
                'date_stop': '2019-12-31',
            }
        )
        self.account_period_model.create({
            'name': 'Period 05/2019',
            'code': '05/2019',
            'date_start': '2019-05-01',
            'date_stop': '2019-05-31',
            'special': False,
            'fiscalyear_id': self.fiscalyear2019.id,
        })

        self.fiscalyear2020 = self.account_fiscalyear_model.create(
            vals={
                'name': '2020',
                'code': '2020',
                'date_start': '2020-01-01',
                'date_stop': '2020-12-31',
            }
        )
        self.account_period_model.create({
            'name': 'Period 10/2020',
            'code': '10/2020',
            'date_start': '2020-10-01',
            'date_stop': '2020-10-31',
            'special': False,
            'fiscalyear_id': self.fiscalyear2020.id,
        })

    def create_attachment(self, name, file_name,
                          datas_fname=None, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_in'
        if datas_fname is None:
            datas_fname = file_name
        attach = self.attach_model.create(
            {
                'name': name,
                'datas': self.getFile(file_name, module_name=module_name)[1],
                'datas_fname': datas_fname
            })
        return attach

    def run_wizard(self, name, file_name, datas_fname=None,
                   mode='import', wiz_values=None, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_in'
        if datas_fname is None:
            datas_fname = file_name

        attach = self.create_attachment(name, file_name,
                                        datas_fname=datas_fname,
                                        module_name=module_name)
        attach_id = attach.id
        if mode == 'import':
            wizard = self.wizard_model.with_context(
                active_ids=[attach_id], active_model='fatturapa.attachment.in'
            ).create(wiz_values or {})
            return wizard.importFatturaPA()
        if mode == 'link':
            wizard = self.wizard_link_model.with_context(
                active_ids=[attach_id], active_model='fatturapa.attachment.in'
            ).create(wiz_values or {})
            return wizard.link()

    def run_wizard_multi(self, file_name_list, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_in'
        active_ids = []
        for file_name in file_name_list:
            active_ids.append(self.attach_model.create(
                {
                    'name': file_name,
                    'datas': self.getFile(file_name, module_name)[1],
                    'datas_fname': file_name
                }).id)
        wizard = self.wizard_model.with_context(
            active_ids=active_ids).create({})
        return wizard.importFatturaPA()

    def setUp(self):
        super(FatturapaCommon, self).setUp()
        self.wizard_model = self.env['wizard.import.fatturapa']
        self.wizard_link_model = self.env['wizard.link.to.invoice']
        self.data_model = self.env['ir.model.data']
        self.attach_model = self.env['fatturapa.attachment.in']
        self.invoice_model = self.env['account.invoice']
        self.account_fiscalyear_model = self.env['account.fiscalyear']
        self.account_period_model = self.env['account.period']
        self.payable_account_id = self.env['account.account'].search([
            ('user_type', '=', self.env.ref(
                'account.data_account_type_payable').id)
        ], limit=1).id
        self.headphones = self.env.ref(
            'product.product_product_7_product_template')
        self.imac = self.env.ref(
            'product.product_product_8_product_template')
        self.service = self.env.ref('product.product_product_1')
        arrotondamenti_attivi_account_id = self.env['account.account'].\
            search([('user_type', '=', self.env.ref(
                'account.data_account_type_income').id)], limit=1).id
        arrotondamenti_passivi_account_id = self.env['account.account'].\
            search([('user_type', '=', self.env.ref(
                'account.data_account_type_expense').id)], limit=1).id
        arrotondamenti_tax_id = self.env['account.tax'].search(
            [('type_tax_use', '=', 'purchase'),
             ('amount', '=', 0.0)], order='sequence', limit=1)
        self.env.user.company_id.arrotondamenti_attivi_account_id = (
            arrotondamenti_attivi_account_id)
        self.env.user.company_id.arrotondamenti_passivi_account_id = (
            arrotondamenti_passivi_account_id)
        self.env.user.company_id.arrotondamenti_tax_id = (
            arrotondamenti_tax_id)
        sconto_maggiorazione_product_id = self.env[
            'product.product'
        ].create({
            'name': 'Global discount',
            'taxes_id': [(6, 0, [self.env.ref(
                'l10n_it_fatturapa.tax_22').id])],
            'supplier_taxes_id': [(6, 0, [self.env.ref(
                'l10n_it_fatturapa.tax_22_acq').id])],
        })
        self.env.user.company_id.sconto_maggiorazione_product_id \
            = sconto_maggiorazione_product_id
        self.provinceSS = self.env['res.country.state'].create({
            'name': 'Sassari',
            'code': 'SS',
            'country_id': self.env.ref('base.it').id
        })
