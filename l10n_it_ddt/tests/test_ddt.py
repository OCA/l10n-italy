# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Francesco Apruzzese
#    Copyright 2015 Apulia Software srl
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################
from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase


class TestDdt(TransactionCase):

    def _create_picking(self):
        return self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            })

    def _create_move(self, picking, product, quantity=1.0):
        src_location = self.env.ref('stock.stock_location_stock')
        dest_location = self.env.ref('stock.stock_location_customers')
        return self.env['stock.move'].create({
            'name': '/',
            'picking_id': picking.id,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'product_uom': product.uom_id.id,
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
            'partner_id': self.partner.id,
            'invoice_state': '2binvoiced',
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
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
            'ddt_type_id': self.env.ref('l10n_it_ddt.ddt_type_ddt').id,
            'carriage_condition_id': self.env.ref(
                'l10n_it_ddt.carriage_condition_PF').id,
            'goods_description_id': self.env.ref(
                'l10n_it_ddt.goods_description_CAR').id,
            'transportation_reason_id': self.env.ref(
                'l10n_it_ddt.transportation_reason_VEN').id,
            'transportation_method_id': self.env.ref(
                'l10n_it_ddt.transportation_method_DES').id,
            }
        if pickings:
            values.update({'picking_ids': [(6, 0, pickings.ids)], })
        return self.ddt_model.create(values)

    def _create_invoice_wizard(self, ddt_ids=None):
        return self.env['ddt.create.invoice'].with_context(
            active_ids=ddt_ids or []
            ).create({
                'journal_id': self.env.ref('account.sales_journal').id,
            })

    def setUp(self):
        super(TestDdt, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.product1 = self.env.ref('product.product_product_25')
        self.product2 = self.env.ref('product.product_product_26')
        self.ddt_model = self.env['stock.picking.package.preparation']
        self.ddt = self._create_ddt()

    def test_invoice_from_ddt_created_by_picking(self):
        # ----- Create a ddt from an existing picking, create invoice and test
        #       it
        picking = self._create_picking()
        picking.action_confirm()
        self._create_move(picking, self.product1, quantity=2)
        picking.action_assign()
        self.ddt.picking_ids = [(6, 0, [picking.id, ])]
        self.ddt.action_put_in_pack()
        self.ddt.action_done()
        wizard = self._create_invoice_wizard([self.ddt.id, ])
        invoice_result = wizard.create_invoice()
        self.assertTrue(invoice_result.get('res_ids', False))
        invoice = self.env[
            invoice_result.get('res_model', 'account.invoice')
            ].browse(invoice_result.get('res_ids', False))
        self.assertEquals(invoice.invoice_line[0].product_id.id,
                          self.ddt.line_ids[0].product_id.id)
        self.assertEquals(invoice.invoice_line[0].quantity,
                          self.ddt.line_ids[0].product_uom_qty)

    def test_invoice_from_ddt_created_by_package_preparation_line(self):
        # ----- Create a ddt with a line that create automatically picking,
        #       create invoice and test it
        self._create_line(self.ddt, self.product1, 2.0)
        self.ddt.action_put_in_pack()
        self.ddt.action_done()
        wizard = self._create_invoice_wizard([self.ddt.id, ])
        invoice_result = wizard.create_invoice()
        self.assertTrue(invoice_result.get('res_ids', False))
        invoice = self.env[
            invoice_result.get('res_model', 'account.invoice')
            ].browse(invoice_result.get('res_ids', False))
        self.assertEquals(invoice.invoice_line[0].product_id.id,
                          self.ddt.line_ids[0].product_id.id)
        self.assertEquals(invoice.invoice_line[0].quantity,
                          self.ddt.line_ids[0].product_uom_qty)

    def test_create_ddt_from_picking(self):
        picking1 = self._create_picking()
        self._create_move(picking1, self.product1, quantity=2)
        picking2 = self._create_picking()
        self._create_move(picking2, self.product2, quantity=3)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [picking1.id, picking2.id]
            }).create({})
        res = wizard.create_ddt()
        ddt = self.ddt_model.browse(res['res_id'])

        self.assertEqual(len(ddt.picking_ids), 2)
        self.assertEqual(len(ddt.line_ids), 2)
        self.assertTrue(picking1 | picking2 == ddt.picking_ids)
        for line in ddt.line_ids:
            if line.product_id == self.product1:
                self.assertEqual(line.product_uom_qty, 2)
            if line.product_id == self.product2:
                self.assertEqual(line.product_uom_qty, 3)

        picking3 = self._create_picking()
        self._create_move(picking3, self.product1, quantity=1)
        self._create_move(picking3, self.product2, quantity=2)
        wizard = self.env['add.pickings.to.ddt'].with_context({
            'active_ids': [picking3.id]
            }).create({'ddt_id': ddt.id})
        wizard.add_to_ddt()

        self.assertEqual(len(ddt.picking_ids), 3)
        self.assertEqual(len(ddt.line_ids), 4)
        self.assertTrue(
            picking1 | picking2 | picking3 == ddt.picking_ids)
        for line in ddt.line_ids:
            if line.product_id == self.product1:
                self.assertTrue(line.product_uom_qty in [1, 2])
            if line.product_id == self.product2:
                self.assertTrue(line.product_uom_qty in [2, 3])

    def test_keep_changed_description(self):
        picking = self._create_picking()
        self._create_move(picking, self.product1, quantity=2)
        picking.action_confirm()
        picking.action_assign()
        self.ddt.picking_ids = [(6, 0, [picking.id, ])]
        self.ddt.line_ids[0].name = 'Changed for test'
        self.ddt.action_put_in_pack()
        self.assertEqual(self.ddt.line_ids[0].name, 'Changed for test')

    def test_invoice_multi_ddt(self):
        picking1 = self._create_picking()
        self._create_move(picking1, self.product1, quantity=2)
        picking2 = self._create_picking()
        self._create_move(picking2, self.product1, quantity=3)
        picking1.action_confirm()
        picking1.action_assign()
        picking2.action_confirm()
        picking2.action_assign()
        wiz_model = self.env['ddt.from.pickings']
        wizard = wiz_model.with_context({
            'active_ids': [picking1.id]
            }).create({})
        res = wizard.create_ddt()
        ddt1 = self.ddt_model.browse(res['res_id'])
        wizard = wiz_model.with_context({
            'active_ids': [picking2.id]
            }).create({})
        res = wizard.create_ddt()
        ddt2 = self.ddt_model.browse(res['res_id'])
        self.assertEqual(ddt1.weight, 0)
        ddt1.action_put_in_pack()
        ddt1.action_done()
        self.assertEqual(ddt1.weight, 0)
        ddt1.weight_manual = 10
        self.assertEqual(ddt1.weight, 10)
        ddt2.action_put_in_pack()
        ddt2.action_done()
        wizard = self._create_invoice_wizard([ddt1.id, ddt2.id])
        invoice_result = wizard.create_invoice()
        invoice = self.env['account.invoice'].browse(
            invoice_result.get('res_ids', False))
        self.assertEqual(len(invoice.invoice_line), 2)
        for line in invoice.invoice_line:
            self.assertEqual(line.product_id.id, self.product1.id)

    def test_picking_multi_ddt(self):
        picking1 = self._create_picking()
        self._create_move(picking1, self.product1, quantity=2)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [picking1.id]
            }).create({})
        wizard.create_ddt()

        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [picking1.id]
            }).create({})
        with self.assertRaises(ValidationError):
            wizard.create_ddt()

        self.ddt_model._default_ddt_type().restrict_pickings = False
        wizard.create_ddt()
