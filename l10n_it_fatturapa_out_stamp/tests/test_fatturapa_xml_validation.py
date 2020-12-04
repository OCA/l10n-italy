# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Alex Comba - Agile Business Group
# Copyright 2020 Marco Colombo - Phi Srl

import base64
import re

from psycopg2 import IntegrityError

from odoo.tools import mute_logger
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon)


class TestFatturaPAXMLValidation(FatturaPACommon):

    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()

    def test_1_xml_export(self):
        self.env.user.company_id.fatturapa_pub_administration_ref = 'F000000111'
        self.env.user.company_id.tax_stamp_product_id = \
            self.env.ref('l10n_it_account_stamp.l10n_it_account_stamp_2_euro')
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
        invoice.tax_stamp = True
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
        self.check_content(xml_content, 'IT06363391001_00001.xml',
                module_name='l10n_it_fatturapa_out_stamp')
