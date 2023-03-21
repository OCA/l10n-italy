# -*- coding: utf-8 -*-

import base64
import tempfile
from odoo.modules import get_module_resource
from odoo.tests.common import SingleTransactionCase


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
            'payment_term': self.env.ref('account.account_payment_term').id,
            'rate_ids': [(0, 0, {'tax': 20.0})],
            'causale_pagamento_id':
                self.env.ref('l10n_it_causali_pagamento.a').id,
        })

    def run_wizard(self, name, file_name, datas_fname=None,
                   mode='import', wiz_values=None, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_in'
        if datas_fname is None:
            datas_fname = file_name
        attach_id = self.attach_model.create(
            {
                'name': name,
                'datas': self.getFile(file_name, module_name=module_name)[1],
                'datas_fname': datas_fname
            }).id
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
        self.payable_account_id = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)
        ], limit=1).id
        self.headphones = self.env.ref(
            'product.product_product_7_product_template')
        self.imac = self.env.ref(
            'product.product_product_8_product_template')
        self.service = self.env.ref('product.product_product_1')
