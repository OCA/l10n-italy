# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo import fields
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

    def _create_order_ddt(self, partner):
        order = self._create_sale_order()
        order.partner_id = partner
        order.onchange_partner_id()
        self.product3.ddt_invoice_exclude = False
        self.product3.invoice_policy = 'order'
        self._create_sale_order_line(order, self.product1)
        self._create_sale_order_line(order, self.product3)
        order.create_ddt = True
        order.action_confirm()
        order.picking_ids.action_assign()
        ddt = order.ddt_ids[0]
        ddt.action_put_in_pack()
        ddt.action_done()
        ddt.to_be_invoiced = True
        return ddt, order

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

    def _create_product_and_lots(self):
        product = self.env['product.product'].create({
            'name': 'Lots product',
            'tracking': 'lot',
            'type': 'product',
        })
        lot1 = self.env['stock.production.lot'].create({
            'name': '0000001',
            'product_id': product.id,
        })
        lot2 = self.env['stock.production.lot'].create({
            'name': '0000002',
            'product_id': product.id,
        })
        inventory = self.env['stock.inventory'].create({
            'name': 'Lots product inventory',
            'filter': 'product',
            'product_id': product.id,
        })
        inventory.action_start()
        inventory.line_ids = [
            (0, 0, {
                'product_id': product.id,
                'prod_lot_id': lot1.id,
                'product_qty': 10,
                'location_id': inventory.location_id.id,
            }),
            (0, 0, {
                'product_id': product.id,
                'prod_lot_id': lot2.id,
                'product_qty': 10,
                'location_id': inventory.location_id.id,
            }),
        ]
        inventory.action_validate()
        return product, lot1, lot2

    def _process_picking_with_lots(
        self, product, lot1, lot2, lot1_qty, lot2_qty
    ):
        picking = self.env['stock.picking'].create(self._get_picking_vals())
        picking.move_ids_without_package = [(0, 0, {
            'product_id': product.id,
            'name': product.name,
            'product_uom_qty': 6,
            'product_uom': product.uom_id.id,
            'pcking_type_id': picking.picking_type_id,
            'location_id': picking.location_id,
            'location_dest_id': picking.location_dest_id,
        })]
        picking.action_confirm()
        picking.action_assign()
        move = picking.move_ids_without_package[0]
        move_line = move.move_line_ids[0]
        move_line.lot_id = lot1.id
        move_line.qty_done = lot1_qty
        move.move_line_ids = [
            (0, 0, {
                'product_uom_id': move.product_uom.id,
                'product_id': product.id,
                'location_id': picking.location_id,
                'location_dest_id': picking.location_dest_id,
                'qty_done': lot2_qty,
                'lot_id': lot2.id,
            }),
        ]
        picking.button_validate()
        return picking

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
        self.partner.ddt_show_price = True
        self.partner2 = self.env.ref('base.res_partner_3')
        self.product1 = self.env.ref('product.product_product_25')
        self.product2 = self.env.ref('product.product_product_27')
        # Virtual Interior Design
        self.product3 = self.env.ref('product.product_product_1')
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
        self.assertTrue(ddt.ddt_show_price)
        ddt.write({
            'carrier_tracking_ref': 'TRACK-1000',
            'dimension': '50x50x10',
        })
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
        ddt._onchange_to_be_invoiced()
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
        self.assertEqual(invoice.dimension, '50x50x10')
        self.assertEqual(invoice.carrier_tracking_ref, 'TRACK-1000')

    def test_action_put_in_pack(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        self.assertTrue('Deco Addict' in self.ddt.display_name)
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.ddt.line_ids[0].name = 'Changed for test'
        self.ddt.action_put_in_pack()
        self.assertEqual(self.ddt.line_ids[0].name, 'Changed for test')
        with self.assertRaises(UserError):
            self.ddt.set_done()
        for picking in self.ddt.picking_ids:
            picking.button_validate()
        self.ddt.set_done()
        self.assertTrue('DDT' in self.ddt.display_name)

    def test_action_put_in_pack_done_pickings_error(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        wiz_vals = self.picking.button_validate()
        # The picking requires further approval
        wiz = self.env[wiz_vals['res_model']] \
            .browse(wiz_vals['res_id'])
        wiz.process()
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.picking.action_done()
        self.assertTrue(self.ddt.check_if_picking_done)
        with self.assertRaises(UserError):
            self.ddt.action_put_in_pack()

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
        order3.weight = 2
        order3.gross_weight = 3
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
            wiz_vals = picking.button_validate()
            # The picking might require further approval
            wiz = self.env[wiz_vals['res_model']] \
                .browse(wiz_vals['res_id'])
            wiz.process()

        # test invoice
        wizard = self.env['sale.advance.payment.inv'].with_context({
            'active_ids': [order3.id]
            }).create({})
        wizard.create_invoices()
        invoice = order3.invoice_ids[0]
        self.assertEqual(
            order3.carriage_condition_id.id, invoice.carriage_condition_id.id)
        self.assertEqual(order3.gross_weight, invoice.gross_weight)
        self.assertEqual(order3.weight, invoice.weight)
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
        self.assertTrue(order4.ddt_show_price)
        self.assertTrue(order5.ddt_show_price)
        ddt4 = order4.ddt_ids[0]
        ddt5 = order5.ddt_ids[0]
        self.assertTrue(ddt4.ddt_show_price)
        self.assertTrue(ddt5.ddt_show_price)
        ddt4.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        ddt5.transportation_reason_id = (
            self.transportation_reason_VEN.id)
        ddt4._onchange_to_be_invoiced()
        ddt5._onchange_to_be_invoiced()
        self.assertTrue(ddt4.to_be_invoiced)
        self.assertTrue(ddt5.to_be_invoiced)
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt4.id, ddt5.id]}).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(invoice.name, invoice.origin)
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
        picking1.action_assign()
        ddt = self._create_ddt(picking1)
        wiz_vals = picking1.button_validate()
        # The picking might require further approval
        wiz = self.env[wiz_vals['res_model']] \
            .browse(wiz_vals['res_id'])
        wiz.process()
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
        order1.picking_ids[0].move_line_ids[0].qty_done = 1
        wiz_id = order1.picking_ids[0].button_validate()['res_id']
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

    def test_ddt_from_scratch(self):
        outgoung_type = self.env['stock.picking.type'].search(
            [('code', '=', 'outgoing')])
        outgoung_type.write({
            'default_location_dest_id': self.env.ref(
                'stock.stock_location_customers').id
        })
        ddt = self._create_ddt()
        ddt.line_ids = [(0, 0, {
            'name': self.product1.name,
            'product_id': self.product1.id,
            'product_uom_qty': 2,
            'product_uom_id': self.product1.uom_id.id,
            'price_unit': 3,
        })]
        ddt.action_put_in_pack()
        ddt.action_done()
        self.assertEqual(ddt.line_ids[0].price_unit, 3)

    def test_order_with_service(self):
        order1 = self._create_sale_order()
        self.product3.ddt_invoice_exclude = False
        self.product3.invoice_policy = 'order'
        self._create_sale_order_line(order1, self.product1)
        self._create_sale_order_line(order1, self.product3)
        order1.create_ddt = True
        order1.action_confirm()
        ddt1 = order1.ddt_ids[0]
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt1.id]}).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(len(invoice.invoice_line_ids), 2)

        order2 = self._create_sale_order()
        self.product3.ddt_invoice_exclude = True
        self._create_sale_order_line(order2, self.product1)
        self._create_sale_order_line(order2, self.product3)
        order2.create_ddt = True
        order2.action_confirm()
        ddt2 = order2.ddt_ids[0]
        invoice_wizard = self.env['ddt.create.invoice'].with_context(
            {'active_ids': [ddt2.id]}).create({})
        action = invoice_wizard.create_invoice()
        invoice_ids = action['domain'][0][2]
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(len(invoice.invoice_line_ids), 1)

    def test_delivered_lots(self):
        product, lot1, lot2 = self._create_product_and_lots()

        picking1 = self._process_picking_with_lots(
            product, lot1, lot2, 3, 3)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [picking1.id]}).create({})
        res = wizard.create_ddt()
        ddt1 = self.ddt_model.browse(res['res_id'])
        quantity_by_lot = ddt1.line_ids[0].quantity_by_lot()
        self.assertEqual(quantity_by_lot, {lot1: '3.00', lot2: '3.00'})

        picking2 = self._process_picking_with_lots(
            product, lot1, lot2, 4, 2)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [picking2.id]}).create({})
        res = wizard.create_ddt()
        ddt2 = self.ddt_model.browse(res['res_id'])
        quantity_by_lot = ddt2.line_ids[0].quantity_by_lot()
        self.assertEqual(quantity_by_lot, {lot1: '4.00', lot2: '2.00'})

    def test_ddt_invoicing(self):
        outgoung_type = self.env['stock.picking.type'].search(
            [('code', '=', 'outgoing')])
        outgoung_type.write({
            'default_location_dest_id': self.env.ref(
                'stock.stock_location_customers').id
        })
        ddt = self._create_ddt()
        ddt.line_ids = [(0, 0, {
            'name': self.product1.name,
            'product_id': self.product1.id,
            'product_uom_qty': 2,
            'product_uom_id': self.product1.uom_id.id,
            'price_unit': 3,
        })]
        ddt.action_put_in_pack()
        ddt.action_done()
        ddt.to_be_invoiced = True
        invoicing_wiz = self.env['ddt.invoicing'].create({
            'date_from': datetime.now().date(),
            'date_to': datetime.now().date(),
        })
        action = invoicing_wiz.create_invoices()
        # context manager translates dates to strings when launching actions
        ctx = action['context'].copy()
        ctx['ddt_date_from'] = fields.Date.to_string(ctx['ddt_date_from'])
        ctx['ddt_date_to'] = fields.Date.to_string(ctx['ddt_date_to'])
        invoice_wiz = self.env['ddt.create.invoice'].with_context(
            ctx).create({})
        res = invoice_wiz.create_invoice()
        self.assertTrue(
            "Relevant period: " in
            self.env['account.invoice'].browse(res['domain'][0][2][0]).name)

    def test_td_multi_invoicing(self):
        """
        TDs to be grouped as follows:
        Order1/TD1 group A (new invoiceA)
        Order2/TD2 group B (new invoiceB)
        Order3/TD3 group A (included in invoice A)

        Check that lines from order1 are only in invoiceA.
        Check that lines from order2 are only in invoiceB.
        Check that lines from order3 are only in invoiceA.
        """

        ddt, order1 = self._create_order_ddt(self.partner)
        ddt2, order2 = self._create_order_ddt(self.partner2)
        ddt3, order3 = self._create_order_ddt(self.partner)

        invoicing_wiz = self.env['ddt.invoicing'].create({
            'date_from': datetime.now().date(),
            'date_to': datetime.now().date(),
        })
        action = invoicing_wiz.create_invoices()
        # context manager translates dates to strings when launching actions
        ctx = action['context'].copy()
        ctx['ddt_date_from'] = fields.Date.to_string(ctx['ddt_date_from'])
        ctx['ddt_date_to'] = fields.Date.to_string(ctx['ddt_date_to'])
        ctx['active_ids'] = [ddt.id, ddt2.id, ddt3.id]
        invoice_wiz = self.env['ddt.create.invoice'].with_context(
            ctx).create({})
        res = invoice_wiz.create_invoice()
        invoice_ids = res['domain'][0][2]
        invoices = self.env['account.invoice'].browse(invoice_ids)

        self.assertEqual(len(invoices), 2)
        invoice_a = ddt.invoice_id
        invoice_b = ddt2.invoice_id
        self.assertNotEqual(invoice_a, invoice_b)

        invoice_a_sale_lines = \
            invoice_a.invoice_line_ids.mapped('sale_line_ids')
        self.assertTrue(set(order1.order_line.ids)
                        .issubset(invoice_a_sale_lines.ids))
        self.assertFalse(set(order2.order_line.ids)
                         .issubset(invoice_a_sale_lines.ids))
        self.assertTrue(set(order3.order_line.ids)
                        .issubset(invoice_a_sale_lines.ids))

        invoice_b_sale_lines = \
            invoice_b.invoice_line_ids.mapped('sale_line_ids')
        self.assertFalse(set(order1.order_line.ids)
                         .issubset(invoice_b_sale_lines.ids))
        self.assertTrue(set(order2.order_line.ids)
                        .issubset(invoice_b_sale_lines.ids))
        self.assertFalse(set(order3.order_line.ids)
                         .issubset(invoice_b_sale_lines.ids))
