# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import new_test_user
from odoo.tests.common import Form

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
        # change user in order to automatically create delivery note
        # when picking is validated
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
        picking.move_ids[0].quantity_done = 1

        res_dict = picking.button_validate()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()
        self.assertTrue(picking.delivery_note_id)
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_ids), 1)
        picking_backorder.move_ids[0].quantity_done = 1
        picking_backorder.button_validate()
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
            groups="stock.group_stock_manager,"
            "l10n_it_delivery_note.use_advanced_delivery_notes",
        )
        # change user in order to automatically create delivery note
        # when picking is validated
        self.env.user = user

        picking = self.env["stock.picking"].create(
            {
                "partner_id": self.recipient.id,
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": self.env.ref("product.product_product_8").name,
                "product_id": self.env.ref("product.product_product_8").id,
                "product_uom_qty": 1,
                "product_uom": self.env.ref("product.product_product_8").uom_id.id,
                "picking_id": picking.id,
                "location_id": self.env.ref("stock.stock_location_stock").id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )

        self.assertEqual(len(picking.move_ids), 1)

        # deliver product
        picking.move_ids.quantity_done = 1
        picking.button_validate()

        # create delivery note with advanced mode
        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                active_ids=[picking.id]
            )
        )
        dn = dn_form.save()
        dn.confirm()

        self.assertTrue(picking.delivery_note_id)
        picking.delivery_note_id.action_confirm()
        self.assertEqual(picking.delivery_note_id.state, "confirm")
        self.assertEqual(picking.delivery_note_id.invoice_status, "no")
