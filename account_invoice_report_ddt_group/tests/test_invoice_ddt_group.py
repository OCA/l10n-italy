# -*- coding: utf-8 -*-
# Author: Francesco Apruzzese
# Copyright 2015 Apulia Software srl
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2016 Andrea Cometa - Apulia Software
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp.tests.common import TransactionCase
from odoo import fields


class TestDdt(TransactionCase):

    def _create_move(self, picking, product, quantity=1.0):
        return self.env['stock.move'].create({
            'name': '/',
            'picking_id': picking.id,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'product_uom': product.uom_id.id,
            'location_id': self.src_location.id,
            'location_dest_id': self.dest_location.id,
            'partner_id': self.partner.id,
            })

    def _create_ddt(self, pickings=None):
        values = {
            'partner_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'ddt_type_id': self.env.ref('l10n_it_ddt.ddt_type_ddt').id,
            'carriage_condition_id': self.carriage_condition_PF.id,
            'goods_description_id': self.goods_description_CAR.id,
            'transportation_reason_id': self.transportation_reason_VEN.id,
            'transportation_method_id': self.transportation_method_DES.id,
            }
        if pickings:
            values.update({'picking_ids': [(6, 0, pickings.ids)], })
        return self.ddt_model.create(values)

    def _create_sale_order(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            })
        order.onchange_partner_id()
        order._convert_to_write(order._cache)
        order.write({
            'carriage_condition_id': self.carriage_condition_PF.id,
            'goods_description_id': self.goods_description_CAR.id,
            'transportation_reason_id': self.transportation_reason_VEN.id,
            'transportation_method_id': self.transportation_method_DES.id,
            })
        return order

    def _create_sale_order_line(self, order, product):
        line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': product.id,
            'product_uom_qty': 10,
            'price_unit': 100,
            })
        line.product_id_change()
        line._convert_to_write(line._cache)
        return line

    def setUp(self):
        super(TestDdt, self).setUp()
        self.carriage_condition_PF = self.env.ref(
            'l10n_it_ddt.carriage_condition_PF')
        self.carriage_condition_PA = self.env.ref(
            'l10n_it_ddt.carriage_condition_PA')
        self.goods_description_CAR = self.env.ref(
            'l10n_it_ddt.goods_description_CAR')
        self.goods_description_BAN = self.env.ref(
            'l10n_it_ddt.goods_description_BAN')
        self.transportation_reason_VEN = self.env.ref(
            'l10n_it_ddt.transportation_reason_VEN')
        self.transportation_reason_VEN.to_be_invoiced = True
        self.transportation_reason_VIS = self.env.ref(
            'l10n_it_ddt.transportation_reason_VIS')
        self.transportation_method_DES = self.env.ref(
            'l10n_it_ddt.transportation_method_DES')
        self.transportation_method_MIT = self.env.ref(
            'l10n_it_ddt.transportation_method_MIT')
        self.src_location = self.env.ref('stock.stock_location_stock')
        self.dest_location = self.env.ref('stock.stock_location_customers')
        self.partner = self.env.ref('base.res_partner_2')
        self.product1 = self.env.ref('product.product_product_4')
        self.product2 = self.env.ref('product.product_product_3')
        self.product1.invoice_policy = 'order'
        self.product2.invoice_policy = 'order'
        self.ddt_model = self.env['stock.picking.package.preparation']

    def test_ddt_group(self):
        order1 = self._create_sale_order()
        self._create_sale_order_line(order1, self.product1)
        order1.action_confirm()

        order2 = self._create_sale_order()
        self._create_sale_order_line(order2, self.product2)
        order2.action_confirm()

        for p in order1.picking_ids | order2.picking_ids:
            p.force_assign()
            p.action_done()

        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [p.id for p in order1.picking_ids]
            }).create({})
        res = wizard.create_ddt()
        self.assertEqual(len(order1.ddt_ids), 1)
        ddt1 = self.ddt_model.browse(res['res_id'])
        ddt1.set_done()

        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [p.id for p in order2.picking_ids]
            }).create({})
        res = wizard.create_ddt()
        self.assertEqual(len(order2.ddt_ids), 1)
        ddt2 = self.ddt_model.browse(res['res_id'])
        ddt2.set_done()

        # test invoice
        ddt1.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        ddt2.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt1.id, ddt2.id]}).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])

        inv_dict = invoice.grouped_lines_by_ddt()
        # dict like
        # {
        #   u'DDT/1 - 13/04/2017': [account.invoice.line(1,)],
        #   u'DDT/2 - 14/04/2017': [account.invoice.line(2,)]
        # }
        ddt1_date = fields.Date.from_string(ddt1.date)
        ddt1_key = '%s - %s' % (
            ddt1.ddt_number, '%s/%s/%s' % (
                ddt1_date.day, ddt1_date.month, ddt1_date.year)
        )
        ddt2_date = fields.Date.from_string(ddt2.date)
        ddt2_key = '%s - %s' % (
            ddt2.ddt_number, '%s/%s/%s' % (
                ddt2_date.day, ddt2_date.month, ddt2_date.year)
        )
        self.assertEqual(
            inv_dict[ddt1_key].values()[0][0].product_id.id, self.product1.id)
        self.assertEqual(
            inv_dict[ddt2_key].values()[0][0].product_id.id, self.product2.id)
