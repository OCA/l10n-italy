# -*- coding: utf-8 -*-
# Copyright 2016 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp import exceptions


class TestDdtDelivery(TransactionCase):

    def _picking_factory(self, partner, carrier):
        return self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'partner_id': partner.id,
            'carrier_id': carrier.id,
        })

    def _move_factory(self, product, qty=5.0):
        return self.env['stock.move'].create({
            'name': '/',
            'product_id': product.id,
            'product_uom_qty': qty,
            'product_uom': product.uom_id.id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
        })

    def setUp(self):
        super(TestDdtDelivery, self).setUp()
        self.product1 = self.env.ref('product.product_product_33')
        self.product2 = self.env.ref('product.product_product_36')
        self.partner1 = self.env.ref('base.res_partner_1')
        self.partner2 = self.env.ref('base.res_partner_2')
        self.carrier1 = self.env.ref('delivery.normal_delivery_carrier')
        self.carrier2 = self.env.ref('delivery.free_delivery_carrier')

    def test_ddt_from_so(self):
        self.so = self.env['sale.order'].create({
            'partner_id': self.partner1.id,
            'carrier_id': self.carrier1.id,
            'create_ddt': True,
        })
        self.sol = self.env['sale.order.line'].create({
            'name': '/',
            'order_id': self.so.id,
            'product_id': self.product1.id,
        })
        self.so.action_button_confirm()
        self.assertEqual(1, len(self.so.ddt_ids))
        self.assertEqual(
            self.so.ddt_ids.carrier_id, self.so.carrier_id.partner_id)

    def test_ddt_from_picking(self):
        pick = self._picking_factory(
            partner=self.partner1, carrier=self.carrier1)
        pick.move_lines = self._move_factory(product=self.product1)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [pick.id]
            }).create({})
        res = wizard.create_ddt()
        ddt = self.env['stock.picking.package.preparation'].browse(
            res['res_id'])
        self.assertEqual(
            ddt.carrier_id, pick.carrier_id.partner_id)

    def test_ddt_from_pickings_with_several_carriers(self):
        pick1 = self._picking_factory(
            partner=self.partner1, carrier=self.carrier1)
        pick1.move_lines = self._move_factory(product=self.product1)
        pick2 = self._picking_factory(
            partner=self.partner1, carrier=self.carrier2)
        pick2.move_lines = self._move_factory(product=self.product2)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [pick1.id, pick2.id]
            }).create({})
        with self.assertRaises(exceptions.Warning) as exc:
            wizard.create_ddt()
        self.assertEqual(
            exc.exception.message,
            'Selected Pickings have different carriers'
        )
