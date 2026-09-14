# Copyright 2024 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, time, timedelta

from odoo import Command, fields
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

    def _create_purchase_order(
        self, product_qty, price_unit, days_ago=0, receive_qty=None
    ):
        """Create and validate a purchase order with backdated delivery

        With `receive_qty`, only that quantity is received and the rest is left
        in a backorder.
        """
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

        if receive_qty is None:
            picking.button_validate()
        else:
            picking.move_ids.quantity = receive_qty
            picking.move_ids.picked = True
            action = picking.button_validate()
            Form.from_action(self.env, action).save().process()

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

    def _set_date(self, picking, date):
        """Backdate a done picking with its moves and move lines"""
        picking.date_done = date
        picking.move_ids.date = date
        picking.move_line_ids.date = date

    def _receive_backorder(self, purchase_order, days_ago=0):
        backorder = purchase_order.picking_ids.filtered(lambda p: p.state != "done")
        backorder.button_validate()
        self._set_date(backorder, fields.Date.today() - timedelta(days=days_ago))

    def _return_to_vendor(self, purchase_order, product_qty, days_ago=0):
        """Return part of the first receipt, updating the purchased quantity"""
        picking = purchase_order.picking_ids.sorted("id")[:1]
        wizard = self.env["stock.return.picking"].create({"picking_id": picking.id})
        wizard.product_return_moves.quantity = product_qty
        return_picking = wizard._create_return()
        return_picking.move_ids.picked = True
        return_picking.button_validate()
        self._set_date(return_picking, fields.Date.today() - timedelta(days=days_ago))

    def _create_bill(self, purchase_order, quantity=None, price_unit=None):
        """Post the bill, or the refund, for what is left to invoice"""
        purchase_order = purchase_order.with_env(self.env)
        previous_bills = purchase_order.invoice_ids
        purchase_order.action_create_invoice()
        bill = purchase_order.invoice_ids - previous_bills
        line_vals = {}
        if quantity is not None:
            line_vals["quantity"] = quantity
        if price_unit is not None:
            line_vals["price_unit"] = price_unit
        bill.write(
            {
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.update(bill.invoice_line_ids.id, line_vals)
                ],
            }
        )
        bill.action_post()
        return bill

    def _create_internal_transfer(self, product_qty, location_dest, days_ago=0):
        move = self.env["stock.move"].create(
            {
                "name": f"Internal transfer {self.product.name}",
                "product_id": self.product.id,
                "product_uom_qty": product_qty,
                "product_uom": self.product.uom_id.id,
                "location_id": self.stock_location.id,
                "location_dest_id": location_dest.id,
            }
        )
        move._action_confirm()
        move._action_assign()
        move.picked = True
        move._action_done()
        move.date = move.move_line_ids.date = fields.Date.today() - timedelta(
            days=days_ago
        )

    def _compute_close_period(self, evaluation_method, close_date, last_closed=None):
        """Start and compute a closing period on the test product only"""
        stock_close_period_form = Form(
            self.env["stock.close.period"].with_user(self.test_user)
        )
        stock_close_period_form.force_evaluation_method = evaluation_method
        stock_close_period_form.name = f"{evaluation_method} {close_date}"
        stock_close_period_form.close_date = close_date
        if last_closed:
            stock_close_period_form.last_closed_id = last_closed
        stock_close_period = stock_close_period_form.save()
        stock_close_period.action_start()
        stock_close_lines = stock_close_period.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        (stock_close_period.line_ids - stock_close_lines).unlink()
        stock_close_period.action_recalculate_purchase()
        return stock_close_period

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

    def test_07_fifo_partially_invoiced_purchase(self):
        """Test FIFO price of a purchase only partially invoiced"""
        purchase_order = self._create_purchase_order(
            product_qty=10, price_unit=10, days_ago=20
        )
        # Only 5 of the 10 received units are invoiced so far
        self._create_bill(purchase_order, quantity=5)

        stock_close_period = self._compute_close_period("fifo", fields.Date.today())
        stock_close_line = stock_close_period.line_ids

        self.assertEqual(stock_close_line.product_qty, 10)
        # The bill is 5@10: the price must not be 50 / 10 ordered units = 5
        self.assertAlmostEqual(stock_close_line.price_unit, 10)

    def test_08_purchase_average_line_received_twice(self):
        """Test purchase average of a purchase line received in 2 shipments"""
        purchase_order = self._create_purchase_order(
            product_qty=10, price_unit=10, days_ago=30, receive_qty=5
        )
        self._receive_backorder(purchase_order, days_ago=25)
        self._create_purchase_order(product_qty=10, price_unit=20, days_ago=20)

        stock_close_period = self._compute_close_period("purchase", fields.Date.today())
        stock_close_line = stock_close_period.line_ids

        self.assertEqual(stock_close_line.product_qty, 20)
        # Average: (10*10 + 10*20) / 20 = 15, the first purchase line must not
        # be counted once per stock move: (200 + 200) / 30 = 13.33
        self.assertAlmostEqual(stock_close_line.cumulative_qty, 20)
        self.assertAlmostEqual(stock_close_line.price_unit, 15)

    def test_09_purchase_average_vendor_refund(self):
        """Test purchase average with goods returned to vendor and refunded"""
        purchase_order = self._create_purchase_order(
            product_qty=10, price_unit=10, days_ago=30
        )
        self._create_bill(purchase_order)
        purchase_order1 = self._create_purchase_order(
            product_qty=10, price_unit=20, days_ago=20
        )
        self._create_bill(purchase_order1)
        self._return_to_vendor(purchase_order1, product_qty=5, days_ago=15)
        refund = self._create_bill(purchase_order1)
        self.assertEqual(refund.move_type, "in_refund")

        stock_close_period = self._compute_close_period("purchase", fields.Date.today())
        stock_close_line = stock_close_period.line_ids

        self.assertEqual(stock_close_line.product_qty, 15)
        # Average: (10*10 + 10*20 - 5*20) / (10 + 10 - 5) = 13.33, the refund
        # must not be added to the purchased amount and quantity
        self.assertAlmostEqual(stock_close_line.cumulative_qty, 15)
        self.assertAlmostEqual(stock_close_line.price_unit, 200 / 15, places=2)

    def test_10_purchase_average_cancelled_bill(self):
        """Test purchase average ignores cancelled bills"""
        purchase_order = self._create_purchase_order(
            product_qty=10, price_unit=10, days_ago=20
        )
        # Bill registered with a wrong price, then cancelled and registered again
        wrong_bill = self._create_bill(purchase_order, price_unit=12)
        wrong_bill.button_draft()
        wrong_bill.button_cancel()
        self._create_bill(purchase_order)

        stock_close_period = self._compute_close_period("purchase", fields.Date.today())
        stock_close_line = stock_close_period.line_ids

        self.assertAlmostEqual(stock_close_line.cumulative_qty, 10)
        self.assertAlmostEqual(stock_close_line.price_unit, 10)

    def test_11_moves_on_close_date(self):
        """Test moves done on the close date are part of the closing quantity"""
        close_date = fields.Date.today() - timedelta(days=5)
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=10)
        self._create_purchase_order(product_qty=10, price_unit=20, days_ago=5)

        stock_close_period = self._compute_close_period("fifo", close_date)
        stock_close_line = stock_close_period.line_ids

        # FIFO evaluates moves until close_date 23:59:59, so they must be in the
        # quantity too, instead of reverting moves from close_date 00:00
        self.assertEqual(stock_close_line.product_qty, 20)
        # FIFO: 10@10 + 10@20 = 300/20 = 15
        self.assertAlmostEqual(stock_close_line.price_unit, 15)

    def test_12_purchase_average_last_close_date(self):
        """Test purchase average does not count again last close date purchases"""
        last_close_date = fields.Date.today() - timedelta(days=100)
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=110)
        purchase_order = self._create_purchase_order(
            product_qty=10, price_unit=20, days_ago=100
        )
        # Received during the day, not at midnight
        self._set_date(
            purchase_order.picking_ids, datetime.combine(last_close_date, time(10))
        )
        self._create_purchase_order(product_qty=10, price_unit=40, days_ago=90)

        stock_close_period = self._compute_close_period("purchase", last_close_date)
        stock_close_period.action_done()
        stock_close_period1 = self._compute_close_period(
            "purchase", fields.Date.today(), last_closed=stock_close_period
        )
        stock_close_line1 = stock_close_period1.line_ids

        # Purchases of last close date are already in the previous average
        self.assertAlmostEqual(stock_close_line1.cumulative_qty, 10)
        self.assertEqual(stock_close_period.line_ids.product_qty, 20)
        self.assertAlmostEqual(stock_close_period.line_ids.price_unit, 15)
        self.assertEqual(stock_close_line1.inventory_qty, 20)
        # Average: (20*15 + 10*40) / 30 = 23.33
        self.assertAlmostEqual(stock_close_line1.price_unit, 700 / 30, places=2)

    def test_13_fifo_stock_in_two_locations(self):
        """Test FIFO evaluates the whole stock of a product in two locations"""
        shelf_location = self.env["stock.location"].create(
            {
                "name": "Shelf 2",
                "usage": "internal",
                "location_id": self.stock_location.id,
            }
        )
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=20)
        self._create_purchase_order(product_qty=10, price_unit=20, days_ago=10)
        self._create_internal_transfer(10, shelf_location, days_ago=5)

        stock_close_period = self._compute_close_period("fifo", fields.Date.today())
        stock_close_lines = stock_close_period.line_ids

        self.assertEqual(
            {(line.location_id, line.product_qty) for line in stock_close_lines},
            {(self.stock_location, 10), (shelf_location, 10)},
        )
        # FIFO: 10@10 + 10@20 = 300/20 = 15 for both locations, not only the
        # last 10 units purchased @20 for the first location stock
        self.assertAlmostEqual(stock_close_period.amount, 300)
        for stock_close_line in stock_close_lines:
            self.assertAlmostEqual(stock_close_line.price_unit, 15)

    def test_14_start_duplicated_close_period(self):
        """Test starting a duplicated closing does not duplicate its lines"""
        shelf_location = self.env["stock.location"].create(
            {
                "name": "Shelf 2",
                "usage": "internal",
                "location_id": self.stock_location.id,
            }
        )
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=20)
        self._create_internal_transfer(5, shelf_location, days_ago=10)
        stock_close_period = self._compute_close_period("fifo", fields.Date.today())
        self.assertEqual(len(stock_close_period.line_ids), 2)

        # Lines are copied with the closing
        stock_close_period1 = stock_close_period.copy()
        self.assertEqual(stock_close_period1.state, "draft")
        self.assertEqual(len(stock_close_period1.line_ids), 2)
        stock_close_period1.action_start()

        stock_close_lines = stock_close_period1.line_ids.filtered(
            lambda x: x.product_id == self.product
        )
        self.assertEqual(
            sorted(
                (line.location_id.id, line.product_qty) for line in stock_close_lines
            ),
            sorted([(self.stock_location.id, 5), (shelf_location.id, 5)]),
        )

    def test_15_lifo_same_day_moves(self):
        """Test LIFO considers incoming moves done before outgoing ones of the day"""
        self._create_purchase_order(product_qty=10, price_unit=10, days_ago=20)
        # Delivery created before the purchase, with the same date
        self._create_delivery_order(product_qty=10, days_ago=10)
        self._create_purchase_order(product_qty=10, price_unit=20, days_ago=10)

        stock_close_period = self._compute_close_period("lifo", fields.Date.today())
        stock_close_line = stock_close_period.line_ids

        self.assertEqual(stock_close_line.product_qty, 10)
        # LIFO: the purchase @20 is delivered in the same day, the stock left
        # comes from the purchase @10
        self.assertAlmostEqual(stock_close_line.price_unit, 10)
