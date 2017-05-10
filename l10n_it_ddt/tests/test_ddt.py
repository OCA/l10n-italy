# -*- coding: utf-8 -*-
# Author: Francesco Apruzzese
# Copyright 2015 Apulia Software srl
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.exceptions import Warning as UserError


class TestDdt(TransactionCase):

    def _get_picking_vals(self):
        return {
            'partner_id': self.partner.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.src_location.id,
            'location_dest_id': self.dest_location.id,
            }

    def _create_picking(self):
        return self.env['stock.picking'].create(self._get_picking_vals())

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

    def _create_line(self, preparation, product=None, quantity=0):
        return self.env['stock.picking.package.preparation.line'].create({
            'name': 'test',
            'product_id': product and product.id or False,
            'product_uom_qty': quantity,
            'product_uom': product and product.uom_id.id or False,
            'package_preparation_id': preparation.id,
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

    def _create_sale_order_line(self, order, product, quantity=1.0):
        line = self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': product.id,
            'product_uom_qty': quantity,
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
        self.partner2 = self.env.ref('base.res_partner_3')
        self.product1 = self.env.ref('product.product_product_25')
        self.product2 = self.env.ref('product.product_product_27')
        self.ddt_model = self.env['stock.picking.package.preparation']
        self.picking = self._create_picking()
        self.move = self._create_move(self.picking, self.product1)
        self.ddt = self._create_ddt()

    def test_create_ddt_from_picking(self):
        self.picking1 = self._create_picking()
        self._create_move(self.picking1, self.product1, quantity=2)
        self.picking2 = self._create_picking()
        self._create_move(self.picking2, self.product2, quantity=3)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [self.picking1.id, self.picking2.id]
            }).create({})
        self.picking2.move_lines[0].partner_id = self.partner2.id
        with self.assertRaises(UserError):
            wizard.create_ddt()
        self.picking2.move_lines[0].partner_id = self.partner.id
        res = wizard.create_ddt()
        ddt = self.ddt_model.browse(res['res_id'])

        self.assertEqual(len(ddt.picking_ids), 2)
        self.assertEqual(len(ddt.line_ids), 2)
        self.assertTrue(self.picking1 | self.picking2 == ddt.picking_ids)
        for line in ddt.line_ids:
            if line.product_id == self.product1:
                self.assertEqual(line.product_uom_qty, 2)
            if line.product_id == self.product2:
                self.assertEqual(line.product_uom_qty, 3)

        self.picking3 = self._create_picking()
        self._create_move(self.picking3, self.product1, quantity=1)
        self._create_move(self.picking3, self.product2, quantity=2)
        self.picking3.move_lines[0].partner_id = self.partner2.id
        self.assertEqual(
            self.picking3.get_ddt_shipping_partner(), self.partner)
        self.picking3.move_lines[1].partner_id = self.partner2.id
        self.assertEqual(
            self.picking3.get_ddt_shipping_partner(), self.partner2)
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [self.picking3.id]
            }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()
        self.picking3.move_lines[0].partner_id = self.partner.id
        self.picking3.move_lines[1].partner_id = self.partner.id
        wizard = self.env['add.pickings.to.ddt'].with_context({
            'active_ids': [self.picking3.id]
            }).create({'ddt_id': ddt.id})
        wizard.add_to_ddt()
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [self.picking3.id]
                }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()

        self.assertEqual(len(ddt.picking_ids), 3)
        self.assertEqual(len(ddt.line_ids), 4)
        self.assertTrue(
            self.picking1 | self.picking2 | self.picking3 == ddt.picking_ids)
        for line in ddt.line_ids:
            if line.product_id == self.product1:
                self.assertTrue(line.product_uom_qty in [1, 2])
            if line.product_id == self.product2:
                self.assertTrue(line.product_uom_qty in [2, 3])
        ddt.on_change_partner()
        self.assertFalse(ddt.carriage_condition_id)
        self.picking3.unlink()
        self.assertEqual(len(ddt.line_ids), 2)
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt.id]}).create({})
        self.assertFalse(ddt.to_be_invoiced)
        with self.assertRaises(UserError):
            invoice_wizard.create_invoice()
        ddt.transportation_reason_id = self.transportation_reason_VEN.id
        self.assertTrue(ddt.to_be_invoiced)
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        self.assertEqual(len(invoice_ids), 1)
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(invoice.partner_id.id, self.partner.id)
        self.assertEqual(len(invoice.invoice_line_ids), 2)
        self.assertTrue(
            self.product1.id in
            [p.id for p in invoice.invoice_line_ids.mapped('product_id')]
        )

    def test_action_put_in_pack(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        self.assertTrue('Agrolait' in self.ddt.display_name)
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.ddt.line_ids[0].name = 'Changed for test'
        self.ddt.action_put_in_pack()
        self.assertEqual(self.ddt.line_ids[0].name, 'Changed for test')
        with self.assertRaises(UserError):
            self.ddt.set_done()
        for picking in self.ddt.picking_ids:
            picking.do_transfer()
        self.ddt.set_done()
        self.assertTrue('DDT' in self.ddt.display_name)

    def test_action_put_in_pack_error(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.ddt.line_ids.unlink()
        with self.assertRaises(UserError):
            self.ddt.action_put_in_pack()

    def test_sale_order(self):
        order1 = self._create_sale_order()
        self._create_sale_order_line(order1, self.product1)
        order1.parcels = 1
        order1.action_confirm()
        order2 = self._create_sale_order()
        self._create_sale_order_line(order2, self.product1)
        order2.parcels = 2
        order2.action_confirm()
        pickings = order1.picking_ids | order2.picking_ids
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [p.id for p in pickings]
            }).create({})
        with self.assertRaises(UserError):
            wizard.create_ddt()
        order2.parcels = 1
        order2.carriage_condition_id = self.carriage_condition_PA.id
        with self.assertRaises(UserError):
            wizard.create_ddt()
        order2.carriage_condition_id = self.carriage_condition_PF.id
        order2.goods_description_id = self.goods_description_BAN.id
        with self.assertRaises(UserError):
            wizard.create_ddt()
        order2.goods_description_id = self.goods_description_CAR.id
        order2.transportation_reason_id = self.transportation_reason_VIS.id
        with self.assertRaises(UserError):
            wizard.create_ddt()
        order2.transportation_reason_id = self.transportation_reason_VEN.id
        order2.transportation_method_id = self.transportation_method_MIT.id
        with self.assertRaises(UserError):
            wizard.create_ddt()
        order2.transportation_method_id = self.transportation_method_DES.id
        res = wizard.create_ddt()
        self.assertEqual(len(order1.ddt_ids), 1)
        ddt = self.ddt_model.browse(res['res_id'])

        action = order1.action_view_ddt()
        self.assertFalse(action['domain'])
        self.assertTrue(action['res_id'])

        # adding picking to DDT
        order3 = self._create_sale_order()
        self._create_sale_order_line(order3, self.product1)
        order3.action_confirm()
        order3.carriage_condition_id = self.carriage_condition_PA.id
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [order3.picking_ids[0].id]
            }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()
        order3.carriage_condition_id = self.carriage_condition_PF.id
        order3.goods_description_id = self.goods_description_BAN.id
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [order3.picking_ids[0].id]
            }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()
        order3.goods_description_id = self.goods_description_CAR.id
        order3.transportation_reason_id = self.transportation_reason_VIS.id
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [order3.picking_ids[0].id]
            }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()
        order3.transportation_reason_id = self.transportation_reason_VEN.id
        order3.transportation_method_id = self.transportation_method_MIT.id
        with self.assertRaises(UserError):
            wizard = self.env['add.pickings.to.ddt'].with_context({
                'active_ids': [order3.picking_ids[0].id]
            }).create({'ddt_id': ddt.id})
            wizard.add_to_ddt()
        order3.transportation_method_id = self.transportation_method_DES.id
        order3.picking_ids.action_confirm()
        order3.picking_ids.action_assign()
        for picking in order3.picking_ids:
            picking.do_transfer()

        # test invoice
        wizard = self.env['sale.advance.payment.inv'].with_context({
            'active_ids': [order3.id]
            }).create({})
        wizard.create_invoices()
        invoice = order3.invoice_ids[0]
        self.assertEqual(
            order3.carriage_condition_id.id, invoice.carriage_condition_id.id)
        invoice._onchange_partner_id()
        self.assertFalse(invoice.carriage_condition_id)

        # testing adding new line to existing picking
        order4 = self._create_sale_order()
        self._create_sale_order_line(order4, self.product1)
        order4.create_ddt = True
        order4.action_confirm()
        self.assertEqual(len(order4.ddt_ids), 1)
        self.assertEqual(len(order4.ddt_ids.line_ids), 1)
        order4.picking_ids[0].write({
            'move_lines': [(0, 0, {
                'name': '/',
                'product_id': self.product1.id,
                'product_uom_qty': 2,
                'product_uom': self.product1.uom_id.id,
                'location_id': self.src_location.id,
                'location_dest_id': self.dest_location.id,
            })]
        })
        self.assertEqual(len(order4.ddt_ids.line_ids), 2)

        # testing creation of picking linking it to existing DDT
        vals = self._get_picking_vals()
        vals['ddt_ids'] = [(4, ddt.id)]
        vals['move_lines'] = [(0, 0, {
            'name': '/',
            'product_id': self.product1.id,
            'product_uom_qty': 3,
            'product_uom': self.product1.uom_id.id,
            'location_id': self.src_location.id,
            'location_dest_id': self.dest_location.id,
        })]
        self.env['stock.picking'].create(vals)
        self.assertEqual(len(order1.ddt_ids.line_ids), 3)

        # another order and another DDT to invoice
        order5 = self._create_sale_order()
        self._create_sale_order_line(order5, self.product1)
        order5.create_ddt = True
        order5.action_confirm()
        ddt4 = order4.ddt_ids[0]
        ddt5 = order5.ddt_ids[0]
        ddt4.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        ddt5.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        self.assertTrue(ddt4.to_be_invoiced)
        self.assertTrue(ddt5.to_be_invoiced)
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt4.id, ddt5.id]}).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(len(order4.order_line.invoice_lines), 1)
        self.assertEqual(len(order5.order_line.invoice_lines), 1)
        self.assertEqual(order4.order_line.qty_invoiced, 1.0)
        self.assertEqual(order5.order_line.qty_invoiced, 1.0)
        # I manually added a line to picking of order4
        self.assertEqual(len(invoice.invoice_line_ids), 3)
        with self.assertRaises(UserError):
            # already invoiced
            invoice_wizard.create_invoice()

    def test_set_done(self):
        picking1 = self._create_picking()
        self._create_move(picking1, self.product1, quantity=2)
        ddt = self._create_ddt(picking1)
        picking1.do_transfer()
        ddt.set_done()
        self.assertTrue('DDT' in ddt.display_name)
        self.assertEqual(ddt.weight, 0)
        ddt.weight_manual = 10
        self.assertEqual(ddt.weight, 10)

    def test_partial_pick(self):
        order1 = self._create_sale_order()
        self._create_sale_order_line(order1, self.product1, quantity=2)
        order1.action_confirm()
        order1.picking_ids[0].action_assign()
        order1.picking_ids[0].pack_operation_product_ids[0].qty_done = 1
        wiz_id = order1.picking_ids[0].do_new_transfer()['res_id']
        wizard = self.env['stock.backorder.confirmation'].browse(wiz_id)
        wizard.process()
        self.assertEqual(len(order1.picking_ids), 2)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [order1.picking_ids[0].id]
            }).create({})
        wizard.create_ddt()
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [order1.picking_ids[1].id]
            }).create({})
        wizard.create_ddt()
        action = order1.action_view_ddt()
        self.assertTrue(action['domain'])
        self.assertFalse(action['res_id'])
