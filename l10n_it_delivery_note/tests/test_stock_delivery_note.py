# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNote(StockDeliveryNoteCommon):

    def setUp(self):
        super().setUp()
        self.partner_shipping = self.create_partner(
            'Shipping Address')
        self.partner_shipping.write({
            'parent_id': self.recipient.id,
            'type': 'delivery',
        })

    # ⇒ "Ordine singolo: consegna parziale"
    def test_partial_delivering_single_so(self):
        #
        #     SO ┐         ┌ DdT
        #        ├ Picking ┘
        #        │
        #        └ Picking ┐
        #                  └ DdT
        #

        # remove use_advanced_delivery_notes group in order to automatically
        # create delivery note when picking is validated
        use_adv_notes_group_id = self.env.ref(
            "l10n_it_delivery_note.use_advanced_delivery_notes").id
        self.env.user.write({'groups_id': [(3, use_adv_notes_group_id)]})

        StockPicking = self.env["stock.picking"]
        StockBackorderConfirmationWizard = self.env['stock.backorder.confirmation']
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

        backorder_wiz_id = picking.button_validate()['res_id']
        backorder_wiz = StockBackorderConfirmationWizard.browse(backorder_wiz_id)
        backorder_wiz.process()
        self.assertTrue(picking.delivery_note_id)
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_lines), 1)
        picking_backorder.move_lines[0].quantity_done = 1
        picking_backorder.button_validate()
        self.assertTrue(picking_backorder.delivery_note_id)

    # ⇒ "Ordine singolo: consegna a indirizzo diverso"
    def test_partner_shipping_delivering_single_so(self):
        use_adv_notes_group_id = self.env.ref(
            "l10n_it_delivery_note.use_advanced_delivery_notes").id
        self.env.user.write({'groups_id': [(3, use_adv_notes_group_id)]})

        StockPicking = self.env["stock.picking"]
        StockBackorderConfirmationWizard = self.env['stock.backorder.confirmation']
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

        backorder_wiz_id = picking.button_validate()['res_id']
        backorder_wiz = StockBackorderConfirmationWizard.browse(backorder_wiz_id)
        backorder_wiz.process()
        self.assertTrue(picking.delivery_note_id)
        self.assertEqual(picking.delivery_note_id.partner_id, self.recipient)
        self.assertEqual(picking.delivery_note_id.partner_shipping_id,
                         self.partner_shipping)
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_lines), 1)
        picking_backorder.move_lines[0].quantity_done = 1
        picking_backorder.button_validate()
        self.assertTrue(picking_backorder.delivery_note_id)
        self.assertEqual(picking_backorder.delivery_note_id.partner_id,
                         self.recipient)
        self.assertEqual(picking_backorder.delivery_note_id.partner_shipping_id,
                         self.partner_shipping)
