# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Alex Comba - Agile Business Group

import base64
import re

from psycopg2 import IntegrityError

from odoo.tools import mute_logger
from .fatturapa_common import FatturaPACommon


class TestDuplicatedAttachment(FatturaPACommon):

    def test_duplicated_attachment(self):
        """Attachment name must be unique"""
        # This test breaks the current transaction
        # and every test executed after this in the
        # same transaction would fail.
        # Note that all the tests in TestFatturaPAXMLValidation
        # are executed in the same transaction.
        self.attach_model.create({'name': 'test_duplicated'})
        with self.assertRaises(IntegrityError) as ie:
            with mute_logger('odoo.sql_db'):
                self.attach_model.create({'name': 'test_duplicated'})
        self.assertEqual(ie.exception.pgcode, '23505')


class TestFatturaPAXMLValidation(FatturaPACommon):

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()

    def test_1_xml_export(self):
        self.env.user.company_id.fatturapa_pub_administration_ref = 'F000000111'
        self.set_sequences(13, '2016-01-07')
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
                    'name': 'Mouse\nOptical',
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
        self.assertFalse(self.attach_model.file_name_exists('00001'))
        res = self.run_wizard(invoice.id)

        self.assertTrue(res)
        attachment = self.attach_model.browse(res['res_id'])
        file_name_match = (
            '^%s_[A-Za-z0-9]{5}.xml$' % self.env.user.company_id.vat)
        # Checking file name randomly generated
        self.assertTrue(re.search(file_name_match, attachment.datas_fname))
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00001.xml')
        self.assertTrue(self.attach_model.file_name_exists('00001'))

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00001.xml')

    def test_2_xml_export(self):
        self.set_sequences(14, '2016-06-15')
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
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00002.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00002.xml')

    def test_3_xml_export(self):
        self.set_sequences(15, '2016-06-15')
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
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00003.xml')
        xml_content = base64.decodebytes(attachment.datas)

        self.check_content(xml_content, 'IT06363391001_00003.xml')

    def test_4_xml_export(self):
        self.set_sequences(16, '2016-06-15')
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
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00004.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00004.xml')

    def test_5_xml_export(self):
        self.env.user.company_id.fatturapa_sender_partner = (
            self.intermediario.id)
        self.set_sequences(17, '2016-06-15')
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
        self.set_e_invoice_file_id(attachment, 'IT03297040366_00005.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT03297040366_00005.xml')

    def test_6_xml_export(self):
        self.product_product_10.default_code = 'ODOOCODE'
        self.product_order_01.barcode = '987654'
        self.set_sequences(13, '2018-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2018-01-07',
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
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse Optical',
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
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00006.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00006.xml')

    def test_7_xml_export(self):
        self.product_product_10.default_code = False
        self.product_order_01.barcode = False
        self.company.partner_id.vat = 'CHE-114.993.395 IVA'
        self.company.partner_id.name = 'Azienda estera'
        self.company.partner_id.city = 'Lugano'
        self.company.partner_id.state_id = False
        self.company.partner_id.country_id = self.env.ref('base.ch').id
        self.company.fatturapa_tax_representative = self.intermediario.id
        self.company.fatturapa_stabile_organizzazione = (
            self.stabile_organizzazione.id)
        self.set_sequences(14, '2018-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2018-01-07',
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
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
            ],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'CHE114993395IVA_00007.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'CHE114993395IVA_00007.xml')

    def test_8_xml_export(self):
        self.tax_22.price_include = True
        self.set_sequences(15, '2018-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2018-01-07',
            'partner_id': self.res_partner_fatturapa_2.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'payment_term_id': self.account_payment_term.id,
            'user_id': self.user_demo.id,
            'type': 'out_invoice',
            'currency_id': self.EUR.id,
            'comment': "firsrt line\n\nsecond line",
            'invoice_line_ids': [
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse Optical',
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
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00008.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00008.xml')

    def test_10_xml_export(self):
        # invoice with descriptive line
        self.set_sequences(10, '2019-08-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2019-08-07',
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
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse\nOptical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_10.id})]
                }),
                (0, 0, {
                    'display_type': 'line_note',
                    'name': 'Notes',
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00010.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00010.xml')

    def test_11_xml_export(self):
        self.set_sequences(11, '2018-01-07')
        self.product_product_10.default_code = 'GH82Ø23€ŦD11'
        self.product_order_01.default_code = 'GZD11'
        partner = self.res_partner_fatturapa_2
        partner.name = 'REMODELAÇÃO DECORAÇÃO ŽALEC LDAŠ'
        partner.street = 'Mžaja ŠtraÇÃ 14'
        partner.zip = 'ES-49714'
        partner.city = 'Šofıa'
        partner.country_id = self.env.ref('base.si').id
        partner.vat = 'SI12345679'
        partner.fiscalcode = False
        partner.onchange_country_id_e_inv()
        partner.write(partner._convert_to_write(partner._cache))
        self.assertEqual(partner.codice_destinatario, 'XXXXXXX')
        invoice = self.invoice_model.create({
            'date_invoice': '2018-01-07',
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
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse Optical Ø23 ß11',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_order_01.id,
                    'name': 'Zed+^ Antiv° (£)',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 4,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00011.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00011.xml')

    def test_12_xml_export(self):
        invoicing_partner = self.env['res.partner'].create({
            'parent_id': self.res_partner_fatturapa_2.id,
            'type': 'invoice',
            'city': 'Sanremo',
            'zip': '18038',
            'country_id': self.env.ref("base.it").id,
            'state_id': self.env.ref("base.state_us_2").id,
            'street': 'Via Roma, 1',
            'codice_destinatario': '0000000',
            'pec_destinatario': 'test-invoice@pec.it',
            'electronic_invoice_use_this_address': True,
        })
        self.set_sequences(12, '2020-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2020-01-07',
            'partner_id': invoicing_partner.id,
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
                    'name': 'Mouse Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00012.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00012.xml')

    def test_13_xml_export(self):
        self.set_sequences(12, '2020-01-07')
        self.tax_00_ns.kind_id = self.env.ref("l10n_it_account_tax_kind.n2_1")
        invoice = self.invoice_model.create({
            'date_invoice': '2020-01-07',
            'partner_id': self.res_partner_fatturapa_5.id,
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
                    'name': 'Mouse Optical',
                    'quantity': 1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_00_ns.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00013.xml')

        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00013.xml')

    def test_14_xml_export(self):
        # invoice with negative qty
        self.set_sequences(14, '2021-01-07')
        invoice = self.invoice_model.create({
            'date_invoice': '2021-01-07',
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
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse\nOptical',
                    'quantity': 3,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_10.id})]
                }),
                (0, 0, {
                    'account_id': self.a_sale.id,
                    'product_id': self.product_product_10.id,
                    'name': 'Mouse\nOptical',
                    'quantity': -1,
                    'uom_id': self.product_uom_unit.id,
                    'price_unit': 10,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_10.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00014.xml')

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00014.xml')

    def test_15_xml_export(self):
        """
￼       create an invoice in USD

￼       expect an XML with values in EUR
￼       """

        usd = self.env.ref("base.USD")
        self.env["res.currency.rate"].create(
            {
                "name": "2021-12-16",
                "rate": 1.17,
                "currency_id": usd.id,
                "company_id": self.env.user.company_id.id,
            }
        )
        self.set_sequences(1, '2021-12-16')
        self.tax_00_ns.kind_id = self.env.ref("l10n_it_account_tax_kind.n3_2")
        invoice = self.invoice_model.create({
            'type': 'out_invoice',
            'currency_id': usd.id,
            'date_invoice': '2021-12-16',
            'partner_id': self.res_partner_fatturapa_0.id,
            'payment_term_id': self.account_payment_term.id,
            'journal_id': self.sales_journal.id,
            'account_id': self.a_recv.id,
            'user_id': self.user_demo.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_product_10.id,
                    'account_id': self.a_sale.id,
                    'name': 'Cabinet with Doors',
                    'quantity': 1,
                    'price_unit': 14.00,
                    'uom_id': self.product_uom_unit.id,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_00_ns.id})]
                })],
        })
        invoice.action_invoice_open()
        self.assertEqual(invoice.invoice_line_ids[0].price_unit, 14.00)

        invoice.company_id.xml_divisa_value = "force_eur"
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00015.xml')
        xml_content = base64.decodebytes(attachment.datas)
        with open("/tmp/IT06363391001_00015.xml", "wb") as o:
            o.write(xml_content)
        self.check_content(xml_content, 'IT06363391001_00015.xml')
        attachment.unlink()

        invoice.company_id.xml_divisa_value = "keep_orig"
        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00015a.xml')
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, 'IT06363391001_00015a.xml')
        attachment.unlink()

    def test_unlink(self):
        e_invoice = self._create_e_invoice()
        e_invoice.unlink()
        self.assertFalse(e_invoice.exists())

    def test_reset_to_ready(self):
        e_invoice = self._create_e_invoice()
        e_invoice.state = 'sender_error'
        e_invoice.reset_to_ready()
        self.assertEqual(e_invoice.state, 'ready')

    def test_validate_invoice(self):
        """
        Check that the invoice used for tests
        is open when validated.
        """
        invoice = self._create_invoice()
        self.assertEqual(invoice.state, 'draft')

        invoice.action_invoice_open()

        self.assertEqual(invoice.state, 'open')
