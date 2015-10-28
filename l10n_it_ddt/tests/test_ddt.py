# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Francesco Apruzzese
#    Copyright 2015 Apulia Software srl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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

    def _create_invoice_wizard(self, picking_ids=None):
        return self.env['ddt.create.invoice'].with_context(
            active_ids=picking_ids or []
            ).create({
                'journal_id': self.env.ref('account.sales_journal').id,
            })

    def setUp(self):
        super(TestDdt, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        self.product1 = self.env.ref('product.product_product_25')
        self.product2 = self.env.ref('product.product_product_26')
        self.ddt_model = self.env['stock.picking.package.preparation']
        self.picking = self._create_picking()
        self.move = self._create_move(self.picking, self.product1)
        self.ddt = self._create_ddt()

    def test_invoice_from_ddt_created_by_picking(self):
        # ----- Create a ddt from an existing picking, create invoice and test
        #       it
        self.picking.action_confirm()
        self.picking.action_assign()
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.ddt.action_put_in_pack()
        self.ddt.action_done()
        wizard = self._create_invoice_wizard([self.ddt.id, ])
        invoice_result = wizard.create_invoice()
        self.assertTrue(invoice_result.get('res_id', False))
        invoice = self.env[
            invoice_result.get('res_model', 'account.invoice')
            ].browse(invoice_result.get('res_id', False))
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
        self.assertTrue(invoice_result.get('res_id', False))
        invoice = self.env[
            invoice_result.get('res_model', 'account.invoice')
            ].browse(invoice_result.get('res_id', False))
        self.assertEquals(invoice.invoice_line[0].product_id.id,
                          self.ddt.line_ids[0].product_id.id)
        self.assertEquals(invoice.invoice_line[0].quantity,
                          self.ddt.line_ids[0].product_uom_qty)

    def test_create_ddt_from_picking(self):
        self.picking1 = self._create_picking()
        self._create_move(self.picking1, self.product1, quantity=2)
        self.picking2 = self._create_picking()
        self._create_move(self.picking2, self.product2, quantity=3)
        wizard = self.env['ddt.from.pickings'].with_context({
            'active_ids': [self.picking1.id, self.picking2.id]
            }).create({})
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

    def test_keep_changed_description(self):
        self.picking.action_confirm()
        self.picking.action_assign()
        self.ddt.picking_ids = [(6, 0, [self.picking.id, ])]
        self.ddt.line_ids[0].name = 'Changed for test'
        self.ddt.action_put_in_pack()
        self.assertEqual(self.ddt.line_ids[0].name, 'Changed for test')
