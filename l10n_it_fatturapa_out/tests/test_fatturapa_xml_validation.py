# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Alex Comba - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import tempfile
from odoo.addons.account.tests.account_test_users import AccountTestUsers
from odoo.modules.module import get_module_resource
from lxml import etree
import shutil
import os


class TestFatturaPAXMLValidation(AccountTestUsers):

    def getFilePath(self, filepath):
        with open(filepath) as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return filepath, out.read()

    def getAttacment(self, name):
        path = get_module_resource(
            'l10n_it_fatturapa_out',
            'tests', 'data', 'attah_base.pdf'
        )
        currDir = os.path.dirname(path)
        new_file = '%s/%s' % (currDir, name)
        shutil.copyfile(path, new_file)
        return self.getFilePath(new_file)

    def getFile(self, filename):
        path = get_module_resource('l10n_it_fatturapa_out',
                                   'tests', 'data', filename)
        return self.getFilePath(path)

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()
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
        self.tax_22 = self.env.ref('l10n_it_fatturapa.tax_22')
        self.tax_22_SP = self.env.ref('l10n_it_fatturapa.tax_22_SP')
        self.res_partner_fatturapa_0 = self.env.ref(
            'l10n_it_fatturapa.res_partner_fatturapa_0')
        self.fiscal_position_sp = self.env.ref(
            'l10n_it_fatturapa.fiscal_position_sp')
        company = self.env.ref('base.main_company')
        company.sp_account_id = self.env['account.account'].search([
            (
                'user_type_id', '=',
                self.env.ref('account.data_account_type_current_assets').id
            )
        ], limit=1)
        self.EUR = self.env.ref('base.EUR')
        self.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [self.EUR.id, company.id])

    def AttachFileToInvoice(self, InvoiceId, filename):
        self.fatturapa_attach.create(
            {
                'name': filename,
                'invoice_id': InvoiceId,
                'datas': self.getAttacment(filename)[1],
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

    def check_content(self, xml_content, file_name):
        parser = etree.XMLParser(remove_blank_text=True)
        test_fatt_data = self.getFile(file_name)[1]
        test_fatt_content = test_fatt_data.decode('base64')
        test_fatt = etree.fromstring(test_fatt_content, parser)
        xml = etree.fromstring(xml_content, parser)
        self.assertEqual(etree.tostring(test_fatt), etree.tostring(xml))

    def test_1_xml_export(self):
        self.set_sequences(1, 13, '2016-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2016-01-07',
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse, Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+ Antivirus',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        self.assertTrue(res)
        attachment = self.attach_model.browse(res['res_id'])
        self.assertEqual(attachment.datas_fname, 'IT06363391001_00001.xml')

        # XML doc to be validated
        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00001.xml')

    def test_2_xml_export(self):
        self.set_sequences(2, 14, '2016-06-15')
        invoice = self.invoice_model.create({
            'date_invoice': '2016-06-15',
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'comment': 'prima riga\nseconda riga',
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse, Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+ Antivirus',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
            'related_documents': [(0, 0, {
                'type': 'order',
                'name': 'PO123',
                'cig': '123',
                'cup': '456',
            })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])

        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00002.xml')

    def test_3_xml_export(self):
        self.set_sequences(3, 15, '2016-06-15')
        invoice = self.invoice_model.create({
            'date_invoice': '2016-06-15',
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'comment': 'prima riga\nseconda riga',
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse, Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'admin_ref': 'D122353',
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+ Antivirus',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
            'related_documents': [(0, 0, {
                'type': 'order',
                'name': 'PO123',
                'cig': '123',
                'cup': '456',
            })],
        })
        invoice.action_invoice_open()
        self.AttachFileToInvoice(invoice.id, 'test1.pdf')
        self.AttachFileToInvoice(invoice.id, 'test2.pdf')
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        xml_content = attachment.datas.decode('base64')

        self.check_content(xml_content, 'IT06363391001_00003.xml')

    def test_4_xml_export(self):
        self.set_sequences(4, 16, '2016-06-15')
        invoice = self.invoice_model.create({
            'date_invoice': '2016-06-15',
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'fiscal_position_id': self.fiscal_position_sp.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse, Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22_SP.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+ Antivirus',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22_SP.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00004.xml')

    def test_5_xml_export(self):
        self.set_sequences(5, 17, '2016-06-15')
        invoice = self.invoice_model.create({
            'date_invoice': '2016-06-15',
            'partner_id': self.res_partner_fatturapa_0.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse, Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'discount': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
            ],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        xml_content = attachment.datas.decode('base64')
        self.check_content(xml_content, 'IT06363391001_00005.xml')
