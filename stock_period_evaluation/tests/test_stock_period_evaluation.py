# Copyright 2024 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import fields
from odoo.tests import Form, TransactionCase


class TestStockPeriodEvaluation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env.ref("base.res_partner_2")
        cls.customer.customer_rank = 1
        cls.buy_route = cls.env.ref("purchase_stock.route_warehouse0_buy")
        cls.vendor = cls.env.ref("base.res_partner_3")

        # Create product with supplier info
        supplierinfo = cls.env["product.supplierinfo"].create(
            {
                "partner_id": cls.vendor.id,
                "delay": 10,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product Test Valuation",
                "standard_price": 55.0,
                "type": "consu",
                "is_storable": True,
                "seller_ids": [(6, 0, [supplierinfo.id])],
                "route_ids": [(6, 0, [cls.buy_route.id])],
            }
        )

        # Create test user with proper permissions
        cls.test_user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_valuation",
                "email": "test@test.email",
                "groups_id": [
                    (4, cls.env.ref("base.group_user").id),
                    (4, cls.env.ref("purchase.group_purchase_user").id),
                    (4, cls.env.ref("stock.group_stock_user").id),
                    (
                        4,
                        cls.env.ref(
                            "stock_period_evaluation.group_stock_period_evaluation_manager"
                        ).id,
                    ),
                ],
            }
        )

        # Get warehouse and locations
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.stock_location = cls.warehouse.lot_stock_id
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.supplier_location = cls.env.ref("stock.stock_location_suppliers")

    def _create_purchase_order(self, product_qty, price_unit, days_ago=0):
        """Create and validate a purchase order with backdated delivery"""
        date_order = fields.Date.today() - timedelta(days=days_ago)

        purchase_order_form = Form(self.env["purchase.order"].with_user(self.test_user))
        purchase_order_form.partner_id = self.vendor
        with purchase_order_form.order_line.new() as order_line:
            order_line.product_id = self.product
            order_line.product_qty = product_qty
            order_line.price_unit = price_unit

        purchase_order = purchase_order_form.save()
        purchase_order.date_order = date_order
        purchase_order.button_confirm()

        # Validate the picking
        self.assertEqual(len(purchase_order.picking_ids), 1)
        picking = purchase_order.picking_ids

        # Set quantities and validate
        for move_line in picking.move_line_ids:
            move_line.quantity = move_line.quantity

        # Backdate the picking if necessary
        if days_ago > 0:
            picking.scheduled_date = date_order
            picking.date_done = date_order

        picking.button_validate()

        # Update move dates
        for move in picking.move_ids:
            move.date = date_order

        for move_line in picking.move_line_ids:
            move_line.date = date_order

        return purchase_order

    def _create_delivery_order(self, product_qty, days_ago=0):
        """Create and validate an outgoing delivery (replaces sale order for testing)"""
        date_order = fields.Date.today() - timedelta(days=days_ago)

        # Create a manual outgoing picking
        picking_type_out = self.env["stock.picking.type"].search(
            [("code", "=", "outgoing"), ("warehouse_id", "=", self.warehouse.id)],
            limit=1,
        )

        picking = self.env["stock.picking"].create(
            {
                "partner_id": self.customer.id,
                "picking_type_id": picking_type_out.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "scheduled_date": date_order,
            }
        )

        # Create stock move
        move = self.env["stock.move"].create(
            {
                "name": f"Test Delivery {self.product.name}",
                "product_id": self.product.id,
                "product_uom_qty": product_qty,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "date": date_order,
            }
        )

        # Confirm and assign
        picking.action_confirm()
        picking.action_assign()

        # Set quantities and validate
        for move_line in picking.move_line_ids:
            move_line.quantity = move_line.quantity

        # Backdate and validate
        if days_ago > 0:
            picking.scheduled_date = date_order
            picking.date_done = date_order

        picking.button_validate()

        # Update dates
        for move in picking.move_ids:
            move.date = date_order

        for move_line in picking.move_line_ids:
            move_line.date = date_order

        return picking

    def _refresh_close_period(self, stock_close_period):
        """Refresh stock close period by canceling and restarting"""
        stock_close_period.action_cancel()
        stock_close_period.action_set_to_draft()
        stock_close_period.action_start()

        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        # Remove other product lines for cleaner testing
        (stock_close_period.line_ids - stock_close_line).unlink()
        return stock_close_line

    def test_01_stock_close_fifo(self):
        """Test FIFO valuation method"""
        # Create initial purchases
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=365)
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=365)

        # Create first closing period
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "fifo"
        stock_close_period_form.name = "FIFO Test Period 1"
        stock_close_period_form.close_date = fields.Date.today() - timedelta(days=300)
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        self.assertTrue(stock_close_period.line_ids)
        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        self.assertEqual(stock_close_line.product_qty, 20)
        stock_close_period.action_recalculate_purchase()
        self.assertEqual(stock_close_line.price_unit, 5)

        stock_close_period.action_done()
        self.assertEqual(stock_close_period.state, "done")

        # Add more purchases
        self._create_purchase_order(product_qty=10, price_unit=7, days_ago=100)
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=90)

        # Create second closing period linked to the first
        stock_close_period_form1 = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form1.force_evaluation_method = "fifo"
        stock_close_period_form1.name = "FIFO Test Period 2"
        stock_close_period_form1.close_date = fields.Date.today()
        stock_close_period_form1.last_closed_id = stock_close_period
        stock_close_period1 = stock_close_period_form1.save()
        stock_close_period1.action_start()

        self.assertTrue(stock_close_period1.line_ids)
        stock_close_line1 = stock_close_period1.line_ids.filtered(
            lambda x: x.product_id == self.product
        )

        self.assertEqual(stock_close_line1.product_qty, 40)
        stock_close_period1.action_recalculate_purchase()
        # FIFO: 20@5 + 10@7 + 10@10 = 270/40 = 6.75
        self.assertEqual(stock_close_line1.price_unit, 6.75)

        # Create delivery to reduce stock
        self._create_delivery_order(product_qty=30, days_ago=80)
        stock_close_line1 = self._refresh_close_period(stock_close_period1)
        self.assertEqual(stock_close_line1.product_qty, 10)
        stock_close_period1.action_recalculate_purchase()
        # FIFO: remaining 10 units are from latest purchase @10
        self.assertAlmostEqual(stock_close_line1.price_unit, 10)

        # Add more purchase
        self._create_purchase_order(product_qty=15, price_unit=12, days_ago=70)
        stock_close_line1 = self._refresh_close_period(stock_close_period1)
        self.assertEqual(stock_close_line1.product_qty, 25)
        stock_close_period1.action_recalculate_purchase()
        # FIFO: 10@10 + 15@12 = 280/25 = 11.2
        self.assertAlmostEqual(stock_close_line1.price_unit, 11.2)

    def test_02_stock_close_lifo(self):
        """Test LIFO valuation method"""
        # Create initial purchases
        self._create_purchase_order(product_qty=10, price_unit=3, days_ago=395)
        self._create_purchase_order(product_qty=10, price_unit=7, days_ago=365)

        # Create first closing period
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "lifo"
        stock_close_period_form.name = "LIFO Test Period 1"
        stock_close_period_form.close_date = fields.Date.today() - timedelta(days=300)
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        self.assertTrue(stock_close_period.line_ids)
        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        self.assertEqual(stock_close_line.product_qty, 20)
        stock_close_period.action_recalculate_purchase()
        # LIFO: 10@7 + 10@3 = 100/20 = 5
        self.assertAlmostEqual(stock_close_line.price_unit, 5)

        stock_close_period.action_done()
        self.assertEqual(stock_close_period.state, "done")

        # Add more purchase
        self._create_purchase_order(product_qty=10, price_unit=7, days_ago=100)

        # Create second closing period
        stock_close_period_form1 = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form1.force_evaluation_method = "lifo"
        stock_close_period_form1.name = "LIFO Test Period 2"
        stock_close_period_form1.close_date = fields.Date.today()
        stock_close_period_form1.last_closed_id = stock_close_period
        stock_close_period1 = stock_close_period_form1.save()
        stock_close_period1.action_start()

        self.assertTrue(stock_close_period1.line_ids)
        stock_close_line1 = stock_close_period1.line_ids.filtered(
            lambda x: x.product_id == self.product
        )

        self.assertEqual(stock_close_line1.product_qty, 30)
        stock_close_period1.action_recalculate_purchase()
        # LIFO: 10@7 + 20@5 = 170/30 = 5.67
        self.assertAlmostEqual(stock_close_line1.price_unit, 5.67, places=2)

        # Add another purchase and test
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=90)
        stock_close_line1 = self._refresh_close_period(stock_close_period1)
        self.assertEqual(stock_close_line1.product_qty, 40)
        stock_close_period1.action_recalculate_purchase()
        # LIFO: 10@10 + 10@7 + 20@5 = 270/40 = 6.75
        self.assertAlmostEqual(stock_close_line1.price_unit, 6.75)

    def test_03_stock_close_purchase_average(self):
        """Test purchase average cost valuation method"""
        # Create initial purchases
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=365)
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=365)

        # Create first closing period with average method
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "purchase"
        stock_close_period_form.name = "Average Test Period 1"
        stock_close_period_form.close_date = fields.Date.today() - timedelta(days=300)
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        self.assertTrue(stock_close_period.line_ids)
        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        self.assertEqual(stock_close_line.product_qty, 20)
        stock_close_period.action_recalculate_purchase()
        self.assertEqual(stock_close_line.price_unit, 5)

        stock_close_period.action_done()
        self.assertEqual(stock_close_period.state, "done")

        # Add more purchases with different prices
        self._create_purchase_order(product_qty=10, price_unit=7, days_ago=100)
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=90)

        # Create second closing period
        stock_close_period_form1 = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form1.force_evaluation_method = "purchase"
        stock_close_period_form1.name = "Average Test Period 2"
        stock_close_period_form1.close_date = fields.Date.today()
        stock_close_period_form1.last_closed_id = stock_close_period
        stock_close_period1 = stock_close_period_form1.save()
        stock_close_period1.action_start()

        self.assertTrue(stock_close_period1.line_ids)
        stock_close_line1 = stock_close_period1.line_ids.filtered(
            lambda x: x.product_id == self.product
        )

        self.assertEqual(stock_close_line1.product_qty, 40)
        stock_close_period1.action_recalculate_purchase()
        # Average: (20*5 + 10*7 + 10*10) / 40 = 270/40 = 6.75
        self.assertEqual(stock_close_line1.price_unit, 6.75)

    def test_04_stock_close_standard(self):
        """Test standard cost valuation method"""
        # Set a standard price on the product
        self.product.standard_price = 8.0

        # Create purchase
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=30)
        self._create_purchase_order(product_qty=10, price_unit=12, days_ago=20)

        # Create closing period with standard method
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "standard"
        stock_close_period_form.name = "Standard Test Period"
        stock_close_period_form.close_date = fields.Date.today()
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        self.assertEqual(stock_close_line.product_qty, 20)
        stock_close_period.action_recalculate_purchase()

        # Standard method should use the product's standard price
        self.assertEqual(stock_close_line.price_unit, 8.0)
        self.assertEqual(stock_close_line.evaluation_method, "standard")

    def test_05_evaluation_details(self):
        """Test that evaluation details are properly populated for FIFO/LIFO"""
        # Create purchases with clear prices
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=30)
        self._create_purchase_order(product_qty=5, price_unit=20, days_ago=20)

        # Create closing period with FIFO
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "fifo"
        stock_close_period_form.name = "Details Test FIFO"
        stock_close_period_form.close_date = fields.Date.today()
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        stock_close_period.action_recalculate_purchase()

        # Check that evaluation details are populated
        self.assertTrue(stock_close_line.evaluation_details)
        self.assertIn("Total:", stock_close_line.evaluation_details)

        # Test LIFO as well
        stock_close_period.force_evaluation_method = "lifo"
        stock_close_period.action_cancel()
        stock_close_period.action_set_to_draft()
        stock_close_period.action_start()

        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        stock_close_period.action_recalculate_purchase()

        # Check that evaluation details are populated for LIFO
        self.assertTrue(stock_close_line.evaluation_details)
        self.assertIn("Total:", stock_close_line.evaluation_details)

    def test_06_category_based_valuation(self):
        """Test category-based automatic valuation method selection"""
        # Set product category to use FIFO
        self.product.categ_id.property_cost_method = "fifo"

        # Create purchases
        self._create_purchase_order(product_qty=10, price_unit=5, days_ago=30)
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=20)

        # Create closing period with no force (use category setup)
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = "no_force"
        stock_close_period_form.name = "Category Based Test"
        stock_close_period_form.close_date = fields.Date.today()
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()

        stock_close_line = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_line).unlink()

        stock_close_period.action_recalculate_purchase()

        # Should use FIFO based on category setting
        # FIFO: 10@5 + 10@10 = 150/20 = 7.5
        self.assertEqual(stock_close_line.price_unit, 7.5)

        # Evaluation details should be populated for FIFO
        self.assertTrue(stock_close_line.evaluation_details)
        self.assertIn("Total:", stock_close_line.evaluation_details)
