# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form, new_test_user

from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNote(StockDeliveryNoteCommon):
    # ⇒ "Ordine singolo: consegna parziale"
    def test_partial_delivering_single_so(self):
        #
        #     SO ┐         ┌ DdT
        #        ├ Picking ┘
        #        │
        #        └ Picking ┐
        #                  └ DdT
        #

        user = new_test_user(
            self.env,
            login="test",
            groups="stock.group_stock_manager",
        )
        self.env.user = user
        StockPicking = self.env["stock.picking"]

        sales_order = self.create_sales_order(
            [
                self.large_desk_line,  # 1
                self.desk_combination_line,  # 1
            ],
        )
        self.assertEqual(len(sales_order.order_line), 2)
        sales_order.action_confirm()
        self.assertEqual(len(sales_order.picking_ids), 1)
        picking = sales_order.picking_ids
        self.assertEqual(len(picking.move_ids), 2)

        # deliver only the first product
        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1

        wizard = Form.from_action(self.env, picking.button_validate()).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()

        dn = Form.from_action(self.env, picking.action_delivery_note_create()).save()
        dn.confirm()
        self.assertTrue(picking.delivery_note_id)
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_ids), 1)
        picking_backorder.move_ids.quantity = False
        picking_backorder.move_ids[0].quantity = 1
        picking_backorder.button_validate()
        dn = Form.from_action(
            self.env, picking_backorder.action_delivery_note_create()
        ).save()
        dn.confirm()
        self.assertTrue(picking_backorder.delivery_note_id)

    # ⇒ "Consegna senza ordine"
    def test_delivery_without_so(self):
        #
        #     Picking ┐
        #             └ DdT
        #
        user = new_test_user(
            self.env,
            login="test",
            groups="stock.group_stock_manager",
        )
        self.env.user = user

        picking = self.create_picking()

        self.assertEqual(len(picking.move_ids), 1)

        # deliver product
        picking.move_ids.quantity = False
        picking.move_ids.quantity = 1
        picking.button_validate()

        dn = Form.from_action(self.env, picking.action_delivery_note_create()).save()
        dn.confirm()
        self.assertTrue(picking.delivery_note_id)
        picking.delivery_note_id.action_confirm()
        self.assertEqual(picking.delivery_note_id.state, "confirm")
        self.assertEqual(picking.delivery_note_id.invoice_status, "no")

        test_company = self.env["res.company"].create({"name": "Test Company"})
        with self.assertRaises(UserError) as exc:
            picking.delivery_note_id.write({"company_id": test_company.id})
        exc_message = exc.exception.args[0]
        self.assertIn("type_id", exc_message)
        self.assertIn("picking_ids", exc_message)
        self.assertIn("belongs to another company", exc_message)

    def test_delivery_action_confirm(self):
        user = new_test_user(
            self.env,
            login="test",
            groups="stock.group_stock_manager",
        )
        self.env.user = user

        picking = self.create_picking(
            carrier_id=self.env.ref("delivery.delivery_carrier").id
        )

        picking.move_ids.quantity = False
        picking.move_ids.quantity = 1
        picking.button_validate()

        dn = Form.from_action(self.env, picking.action_delivery_note_create()).save()
        dn.confirm()

        delivery_note_id = picking.delivery_note_id
        product_product_delivery_normal = self.env["product.product"].create(
            {
                "name": "Normal Delivery Charges",
                "default_code": "Delivery_008",
                "type": "service",
                "categ_id": self.env.ref("delivery.product_category_deliveries").id,
                "sale_ok": False,
                "purchase_ok": False,
                "invoice_policy": "order",
                "list_price": 10.0,
            }
        )
        normal_delivery_carrier = self.env["delivery.carrier"].create(
            {
                "name": "Normal Delivery Charges",
                "fixed_price": 10.0,
                "sequence": 3,
                "delivery_type": "fixed",
                "product_id": product_product_delivery_normal.id,
            }
        )
        new_picking = self.create_picking(carrier_id=normal_delivery_carrier.id)
        picking.move_ids.quantity = False
        picking.move_ids.quantity = 1
        new_picking.button_validate()

        delivery_note_id.write({"picking_ids": [(4, new_picking.id)]})

        warning_context = delivery_note_id.action_confirm().get("context")
        self.assertTrue(warning_context)
        self.assertIn(
            "contains pickings related to different delivery methods",
            warning_context.get("default_warning_message"),
        )

        picking.carrier_id = self.env.ref("delivery.free_delivery_carrier").id
        new_picking.carrier_id = self.env.ref("delivery.free_delivery_carrier").id
        delivery_note_id.carrier_id = self.env.ref(
            "l10n_it_delivery_note.partner_carrier_2"
        ).id

        warning_context = delivery_note_id.action_confirm().get("context")
        self.assertTrue(warning_context)
        self.assertIn(
            "The carrier set in Delivery Note is "
            "different from the carrier set in picking(s)",
            warning_context.get("default_warning_message"),
        )

        delivery_note_id.delivery_method_id = self.env.ref(
            "delivery.free_delivery_carrier"
        ).id
        picking.carrier_id = self.env.ref("delivery.delivery_carrier").id
        new_picking.carrier_id = self.env.ref("delivery.free_delivery_carrier").id
        warning_context = delivery_note_id.action_confirm().get("context")
        self.assertTrue(warning_context)
        self.assertIn(
            "contains pickings related to different "
            "delivery methods from the same transporter",
            warning_context.get("default_warning_message"),
        )

        new_picking.carrier_id = self.env.ref("delivery.delivery_carrier").id
        delivery_note_id.delivery_method_id = self.env.ref(
            "delivery.free_delivery_carrier"
        ).id
        delivery_note_id.carrier_id = self.env.ref(
            "l10n_it_delivery_note.partner_carrier_1"
        ).id
        warning_context = delivery_note_id.action_confirm().get("context")
        self.assertTrue(warning_context)
        self.assertIn(
            "The shipping method set in Delivery Note is "
            "different from the shipping method set in picking(s)",
            warning_context.get("default_warning_message"),
        )

    def test_delivery_action_confirm_without_ref(self):
        user = new_test_user(
            self.env,
            login="test",
            groups="stock.group_stock_manager,"
            "l10n_it_delivery_note.group_required_partner_ref",
        )
        self.env.user = user

        picking = self.create_picking(
            picking_type_id=self.env.ref("stock.picking_type_in").id,
            carrier_id=self.env.ref("delivery.delivery_carrier").id,
        )
        picking.move_ids.quantity = False
        picking.move_ids.quantity = 1
        picking.button_validate()

        dn = Form.from_action(self.env, picking.action_delivery_note_create()).save()
        dn.confirm()

        delivery_note_id = picking.delivery_note_id

        with self.assertRaises(UserError) as exc:
            delivery_note_id.action_confirm()
        exc_message = exc.exception.args[0]
        self.assertIn("The field 'Partner reference' is mandatory", exc_message)

        delivery_note_id.partner_ref = "Reference #1234"
        delivery_note_id.action_confirm()
