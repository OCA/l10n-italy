# -*- coding: utf-8 -*-

import base64
import tempfile
from lxml import etree
import shutil
import os
from odoo.modules.module import get_module_resource
from odoo.addons.account.tests.account_test_users import AccountTestUsers


class FatturaPACommon(AccountTestUsers):

    def setUp(self):
        super(FatturaPACommon, self).setUp()
        self.wizard_model = self.env['wizard.export.fatturapa']
        self.data_model = self.env['ir.model.data']
        self.attach_model = self.env['fatturapa.attachment.out']
        self.invoice_model = self.env['account.invoice']
        self.fatturapa_attach = self.env['fatturapa.attachments']
        self.context = {}
        self.maxDiff = None
        self.sales_journal = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        account_user_type = self.env.ref(
            'account.data_account_type_receivable')
        self.a_recv = self.account_model.sudo(self.account_manager.id).create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=account_user_type.id,
                reconcile=True,
            ))
        self.a_sale = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_revenue').id)
        ], limit=1)
        self.account_payment_term = self.env.ref(
            'account.account_payment_term')
        self.user_demo = self.env.ref('base.user_demo')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_product_10 = self.env.ref('product.product_product_10')
        self.product_order_01 = self.env.ref('product.product_order_01')
        self.product_product_10.default_code = False
        self.product_product_10.barcode = False
        self.product_order_01.default_code = False
        self.product_order_01.barcode = False
        self.tax_22 = self.env.ref('l10n_it_fatturapa.tax_22')
        self.tax_22_SP = self.env.ref('l10n_it_fatturapa.tax_22_SP')
        self.res_partner_fatturapa_0 = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_0')
        self.res_partner_fatturapa_2 = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_2')
        self.intermediario = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_1')
        self.stabile_organizzazione = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_3')
        self.fiscal_position_sp = self.env.ref(
            'l10n_it_fatturapa.fiscal_position_sp')
        self.company = self.env.ref('base.main_company')
        self.company.sp_account_id = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id
            )
        ], limit=1)
        self.EUR = self.env.ref('base.EUR')
        self.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [self.EUR.id, self.company.id])

    def AttachFileToInvoice(self, InvoiceId, filename):
        self.fatturapa_attach.create(
            {
                'name': filename,
                'invoice_id': InvoiceId,
                'datas': self.getAttachment(filename)[1],
                'datas_fname': filename
            }
        )

    def set_sequences(self, file_number, invoice_number, dt):
        seq_pool = self.env['ir.sequence']
        seq_id = self.data_model.xmlid_to_res_id(
            'l10n_it_fatturapa.seq_fatturapa')
        ftpa_seq = seq_pool.browse(seq_id)
        ftpa_seq.write({
            'implementation': 'no_gap',
            'number_next_actual': file_number, })
        inv_seq = seq_pool.search([('name', '=', 'Customer Invoices')])[0]
        seq_date = self.env['ir.sequence.date_range'].search([
            ('sequence_id', '=', inv_seq.id),
            ('date_from', '<=', dt),
            ('date_to', '>=', dt),
        ], limit=1)
        if not seq_date:
            seq_date = inv_seq._create_date_range_seq(dt)
        seq_date.number_next_actual = invoice_number

    def run_wizard(self, invoice_id):
        wizard = self.wizard_model.create({})
        return wizard.with_context(
            {'active_ids': [invoice_id]}).exportFatturaPA()

    def check_content(self, xml_content, file_name, module_name=None):
        parser = etree.XMLParser(remove_blank_text=True)
        test_fatt_data = self.getFile(file_name, module_name=module_name)[1]
        test_fatt_content = test_fatt_data.decode('base64')
        test_fatt = etree.fromstring(test_fatt_content, parser)
        xml = etree.fromstring(xml_content, parser)
        self.assertEqual(etree.tostring(test_fatt), etree.tostring(xml))

    def getFilePath(self, filepath):
        with open(filepath) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return filepath, out.read()

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out'
        path = get_module_resource(
            module_name, 'tests', 'data', 'attah_base.pdf'
        )
        currDir = os.path.dirname(path)
        new_file = '%s/%s' % (currDir, name)
        shutil.copyfile(path, new_file)
        return self.getFilePath(new_file)

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = 'l10n_it_fatturapa_out'
        path = get_module_resource(module_name, 'tests', 'data', filename)
        return self.getFilePath(path)
