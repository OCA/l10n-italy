# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import codecs
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon)


class TestInvoiceTripleDiscount(FatturaPACommon):

    def setUp(self):
        super(TestInvoiceTripleDiscount, self).setUp()

    def test_xml_export_triple_discount(self):
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
                    'discount': 50,
                    'discount2': 50,
                    'discount3': 50,
                    'invoice_line_tax_ids': [(6, 0, {
                        self.tax_22.id})]
                })],
        })
        invoice.action_invoice_open()
        res = self.run_wizard(invoice.id)

        self.assertTrue(res)
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00001.xml')

        # XML doc to be validated
        xml_content = codecs.decode(attachment.datas, 'base64')
        self.check_content(xml_content, 'IT06363391001_00001.xml',
                           module_name='l10n_it_fatturapa_out_triple_discount')
