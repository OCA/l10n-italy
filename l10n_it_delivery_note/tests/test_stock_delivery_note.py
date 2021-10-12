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
        self.assertEqual(len(picking.move_lines), 2)

        # deliver only the first product
        picking.move_lines[0].quantity_done = 1

        res_dict = picking.button_validate()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()
        self.assertTrue(picking.delivery_note_id)
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_lines), 1)
        picking_backorder.move_lines[0].quantity_done = 1
        picking_backorder.button_validate()
        self.assertTrue(picking_backorder.delivery_note_id)
