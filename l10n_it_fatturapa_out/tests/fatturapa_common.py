# -*- coding: utf-8 -*-

import base64
import tempfile
from lxml import etree
import shutil
import os
from openerp.modules.module import get_module_resource
from openerp.tests.common import TransactionCase


class FatturaPACommon(TransactionCase):

    def setUp(self):
        super(FatturaPACommon, self).setUp()
        self.seq_model = self.env['ir.sequence']
        self.res_user_model = self.env['res.users']
        self.company = self.env.ref('base.main_company')
        self.account_model = self.env['account.account']
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
        res_users_account_user = self.env.ref('account.group_account_user')
        res_users_account_manager = self.env.ref(
            'account.group_account_manager')
        partner_manager = self.env.ref('base.group_partner_manager')
        self.account_user = self.res_user_model.with_context(
            {'no_reset_password': True}).create(dict(
                name="Accountant",
                company_id=self.company.id,
                login="acc",
                email="accountuser@yourcompany.com",
                groups_id=[(6, 0, [
                    res_users_account_user.id, partner_manager.id])]
            ))
        self.account_manager = self.res_user_model.with_context(
            {'no_reset_password': True}).create(dict(
                name="Adviser",
                company_id=self.company.id,
                login="fm",
                email="accountmanager@yourcompany.com",
                groups_id=[
                    (6, 0, [res_users_account_manager.id, partner_manager.id])]
            ))
        self.a_recv = self.account_model.sudo(self.account_manager.id).create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type=account_user_type.id,
                reconcile=True,
            ))
        self.a_sale = self.account_model.search([
            (
                'user_type', '=',
                self.env.ref('account.data_account_type_income').id)
        ], limit=1)
        self.account_payment_term = self.env.ref(
            'account.account_payment_term')
        self.user_demo = self.env.ref('base.user_demo')
        self.product_uom_unit = self.env.ref('product.product_uom_unit')
        self.product_product_10 = self.env.ref('product.product_product_10')
        self.product_order_01 = self.env.ref('product.product_product_1')
        self.product_product_10.default_code = False
        self.product_product_10.ean13 = False
        self.product_order_01.default_code = False
        self.product_order_01.ean13 = False
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
        self.res_partner_fatturapa_4 = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_4')
        self.fiscal_position_sp = self.env.ref(
            'l10n_it_fatturapa.fiscal_position_sp')
        self.company.sp_account_id = self.env.ref('account.ova')
        self.EUR = self.env.ref('base.EUR')
        # United Arab Emirates currency
        self.AED = self.env.ref('base.AED')
        self.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [self.EUR.id, self.company.id])
        obj_acc_fiscalyear = self.env['account.fiscalyear']
        self.fiscalyear = obj_acc_fiscalyear.create(
            vals={
                'name': '2016',
                'code': '2016',
                'date_start': '2016-01-01',
                'date_stop': '2016-12-31',
            }
        )
        self.fiscalyear1 = obj_acc_fiscalyear.create(
            vals={
                'name': '2018',
                'code': '2018',
                'date_start': '2018-01-01',
                'date_stop': '2018-12-31',
            }
        )
        period_obj = self.env['account.period']
        self.period = period_obj.create({
            'name': "Period 01/2016",
            'code': '01/2016',
            'date_start': '2016-01-01',
            'date_stop': '2016-01-31',
            'special': False,
            'fiscalyear_id': self.fiscalyear.id,
        })
        self.period1 = period_obj.create({
            'name': "Period 06/2016",
            'code': '06/2016',
            'date_start': '2016-06-01',
            'date_stop': '2016-06-30',
            'special': False,
            'fiscalyear_id': self.fiscalyear.id,
        })
        self.period2 = period_obj.create({
            'name': "Period 01/2018",
            'code': '01/2018',
            'date_start': '2018-01-01',
            'date_stop': '2018-01-31',
            'special': False,
            'fiscalyear_id': self.fiscalyear1.id,
        })
        self.period3 = period_obj.create({
            'name': "Period 02/2018",
            'code': '02/2018',
            'date_start': '2018-02-01',
            'date_stop': '2018-02-28',
            'special': False,
            'fiscalyear_id': self.fiscalyear1.id,
        })
        self.pricelist = self.env.ref('product.list0')

    def AttachFileToInvoice(self, InvoiceId, filename):
        self.fatturapa_attach.create(
            {
                'name': filename,
                'invoice_id': InvoiceId,
                'datas': self.getAttachment(filename)[1],
                'datas_fname': filename
            }
        )

    def set_sequences(self, file_number, invoice_number, year):
        seq_id = self.data_model.xmlid_to_res_id(
            'l10n_it_fatturapa.seq_fatturapa')
        ftpa_seq = self.seq_model.browse(seq_id)
        ftpa_seq.write({
            'implementation': 'no_gap',
            'number_next_actual': file_number, })
        inv_seq = self.seq_model.search([(
            'name', '=', 'Account Default Sales Journal')])[0]
        inv_seq.write({
            'prefix': 'INV/%s/' % year,
            'padding': 4,
            'implementation': 'no_gap', })
        inv_seq.number_next_actual = invoice_number

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
