import codecs
from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import (
    FatturaPACommon)


class TestInvoiceDDT(FatturaPACommon):

    def setUp(self):
        super(TestInvoiceDDT, self).setUp()
        self.carriage_condition_PF = self.env.ref(
            'l10n_it_ddt.carriage_condition_PF')
        self.goods_description_CAR = self.env.ref(
            'l10n_it_ddt.goods_description_CAR')
        self.transportation_reason_VEN = self.env.ref(
            'l10n_it_ddt.transportation_reason_VEN')
        self.transportation_reason_VEN.to_be_invoiced = True
        self.transportation_method_DES = self.env.ref(
            'l10n_it_ddt.transportation_method_DES')

    def test_e_invoice_ddt(self):
        # 2 ordini, 2 DDT e 1 fattura differita
        self.env.ref('product.list0').currency_id = self.EUR.id
        self.so1 = self.env['sale.order'].create({
            'partner_id': self.res_partner_fatturapa_2.id,
            'partner_invoice_id': self.res_partner_fatturapa_2.id,
            'partner_shipping_id': self.res_partner_fatturapa_2.id,
            'order_line': [(0, 0, {
                'name': 'Mouse Optical',
                'product_id': self.product_product_10.id, 'product_uom_qty': 2,
                'product_uom': self.product_uom_unit.id, 'price_unit': 10,
                'tax_id': [(6, 0, {self.tax_22.id})]
            })],
            'pricelist_id': self.env.ref('product.list0').id,
            'carriage_condition_id': self.carriage_condition_PF.id,
            'goods_description_id': self.goods_description_CAR.id,
            'transportation_reason_id': self.transportation_reason_VEN.id,
            'transportation_method_id': self.transportation_method_DES.id,
        })
        self.so2 = self.env['sale.order'].create({
            'partner_id': self.res_partner_fatturapa_2.id,
            'partner_invoice_id': self.res_partner_fatturapa_2.id,
            'partner_shipping_id': self.res_partner_fatturapa_2.id,
            'order_line': [(0, 0, {
                'name': 'Mouse Optical',
                'product_id': self.product_product_10.id, 'product_uom_qty': 3,
                'product_uom': self.product_uom_unit.id, 'price_unit': 10,
                'tax_id': [(6, 0, {self.tax_22.id})]
            })],
            'pricelist_id': self.env.ref('product.list0').id,
            'carriage_condition_id': self.carriage_condition_PF.id,
            'goods_description_id': self.goods_description_CAR.id,
            'transportation_reason_id': self.transportation_reason_VEN.id,
            'transportation_method_id': self.transportation_method_DES.id,
        })
        self.so1.action_confirm()
        self.so2.action_confirm()
        self.so1.picking_ids.move_lines[0].move_line_ids[0].qty_done = 2.0
        self.so2.picking_ids.move_lines[0].move_line_ids[0].qty_done = 3.0
        self.env['ddt.from.pickings'].with_context({
            'active_ids': self.so1.picking_ids.ids
            }).create({}).create_ddt()
        self.env['ddt.from.pickings'].with_context({
            'active_ids': self.so2.picking_ids.ids
        }).create({}).create_ddt()
        (self.so1.picking_ids | self.so2.picking_ids).action_done()
        self.so1.ddt_ids[0].date = '2018-01-07'
        self.so2.ddt_ids[0].date = '2018-01-07'
        self.so1.ddt_ids[0].ddt_number = 'DDT/0100'
        self.so2.ddt_ids[0].ddt_number = 'DDT/0101'
        self.so1.ddt_ids[0].set_done()
        self.so2.ddt_ids[0].set_done()
        # Set sequence to have the expected order in XML
        self.so1.ddt_ids.line_ids[0].sequence = 1
        self.so2.ddt_ids.line_ids[0].sequence = 2
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': (self.so1.ddt_ids | self.so2.ddt_ids).ids}
        ).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.set_sequences(13, '2018-01-07')
        invoice.date_invoice = '2018-01-07'
        invoice.action_invoice_open()
        wizard = self.wizard_model.with_context(
            {'active_ids': [invoice.id]}
        ).create({})
        # default_get must set include_ddt_data
        self.assertEqual(wizard.include_ddt_data, 'dati_ddt')
        res = wizard.exportFatturaPA()
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00006.xml')
        xml_content = codecs.decode(attachment.datas, 'base64')
        self.assertEqual(
            attachment.datas_fname, 'IT06363391001_00006.xml')
        self.check_content(
            xml_content, 'IT06363391001_00006.xml',
            module_name='l10n_it_fatturapa_out_ddt'
        )

        # fattura accompagnatoria
        self.so3 = self.env['sale.order'].create({
            'partner_id': self.res_partner_fatturapa_2.id,
            'partner_invoice_id': self.res_partner_fatturapa_2.id,
            'partner_shipping_id': self.res_partner_fatturapa_2.id,
            'order_line': [(0, 0, {
                'name': 'Mouse Optical',
                'product_id': self.product_product_10.id, 'product_uom_qty': 2,
                'product_uom': self.product_uom_unit.id, 'price_unit': 10,
                'tax_id': [(6, 0, {self.tax_22.id})]
            })],
            'pricelist_id': self.env.ref('product.list0').id,
            'carriage_condition_id': self.carriage_condition_PF.id,
            'goods_description_id': self.goods_description_CAR.id,
            'transportation_reason_id': self.transportation_reason_VEN.id,
            'transportation_method_id': self.transportation_method_DES.id,
        })
        self.so3.action_confirm()
        self.so3.picking_ids.move_lines[0].move_line_ids[0].qty_done = 2.0
        self.env['ddt.from.pickings'].with_context({
            'active_ids': self.so3.picking_ids.ids
            }).create({}).create_ddt()
        self.so3.picking_ids[0].action_done()
        self.so3.ddt_ids[0].carrier_id = self.intermediario.id
        self.so3.ddt_ids[0].set_done()
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': self.so3.ddt_ids.ids}
        ).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.set_sequences(14, '2018-01-07')
        invoice.date_invoice = '2018-01-07'
        invoice.action_invoice_open()
        wizard = self.wizard_model.with_context(
            {'active_ids': [invoice.id]}
        ).create({})
        wizard.include_ddt_data = 'dati_trasporto'
        res = wizard.exportFatturaPA()
        attachment = self.attach_model.browse(res['res_id'])
        self.set_e_invoice_file_id(attachment, 'IT06363391001_00007.xml')
        xml_content = codecs.decode(attachment.datas, 'base64')
        self.assertEqual(
            attachment.datas_fname, 'IT06363391001_00007.xml')
        self.check_content(
            xml_content, 'IT06363391001_00007.xml',
            module_name='l10n_it_fatturapa_out_ddt'
        )
