from datetime import datetime, timedelta
from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNoteInvoicingTest(StockDeliveryNoteCommon):

    # ⇒ "Ordine singolo: fatturazione completa"
    def test_complete_invoicing_single_so(self):
        #
        #     SO ┐         ┌ DdT
        #        └ Picking ┘
        #

        sales_order = self.create_sales_order([
            self.desk_combination_line,
            self.right_corner_desk_line,
            self.large_cabinet_line,
            self.large_desk_line
        ])
        self.assertEqual(len(sales_order.order_line), 4)

        sales_order.action_confirm()
        self.add_downpayment_line(sales_order, 'percentage', 10)
        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, 'no')

        downpayment_order_line = sales_order.order_line[4]
        self.assertEqual(downpayment_order_line.invoice_status, 'to invoice')
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        picking = sales_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_lines), 4)

        picking.move_lines[0].quantity_done = 1
        picking.move_lines[1].quantity_done = 2
        picking.move_lines[2].quantity_done = 11
        picking.move_lines[3].quantity_done = 1

        result = picking.button_validate()
        self.assertIsNone(result)

        delivery_note = self.create_delivery_note()
        delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        delivery_note.picking_ids = picking
        delivery_note.action_confirm()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, 'confirm')
        self.assertEqual(delivery_note.invoice_status, 'to invoice')

        delivery_note.action_invoice()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, 'invoiced')
        self.assertEqual(delivery_note.invoice_status, 'invoiced')

        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, 'invoiced')

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 2)

        final_invoice = invoices[0]
        self.assertEqual(len(final_invoice.invoice_line_ids), 6)
        self.assertEqual(final_invoice.delivery_note_ids, delivery_note)

        self.assertEqual(delivery_note.invoice_ids, final_invoice)

        #
        # Linea 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Linea 2
        #
        order_line = sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 2)

        delivery_note_line = delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Linea 3
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 11)

        delivery_note_line = delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 11)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 11)

        #
        # Linea 4
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Linea 5 (Downpayment)
        #
        order_line = sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids \
            .filtered(lambda l: l.sale_line_id == order_line)

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Linea 6 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, delivery_note)

    # ⇒ "Ordine singolo: fatturazione parziale"
    def test_partial_invoicing_single_so(self):
        #
        #     SO ┐         ┌ DdT
        #        ├ Picking ┘
        #        │
        #        └ Picking ┐
        #                  └ DdT
        #

        StockPicking = self.env['stock.picking']
        StockBackorderConfirmationWizard = self.env[
            'stock.backorder.confirmation']

        sales_order = self.create_sales_order([
            self.customizable_desk_line,
            self.right_corner_desk_line,
            self.large_cabinet_line,
            self.storage_box_line
        ])
        self.assertEqual(len(sales_order.order_line), 4)

        sales_order.action_confirm()
        self.add_downpayment_line(sales_order, 'percentage', 10)
        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, 'no')

        downpayment_order_line = sales_order.order_line[4]
        self.assertEqual(downpayment_order_line.invoice_status, 'to invoice')
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        picking = sales_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_lines), 4)

        picking.move_lines[0].quantity_done = 2  # 3
        picking.move_lines[1].quantity_done = 2
        picking.move_lines[2].quantity_done = 6  # 11
        picking.move_lines[3].quantity_done = 3  # 5

        wizard = StockBackorderConfirmationWizard.create({
            'pick_ids': [(4, picking.id)]
        })
        wizard.process()

        first_delivery_note = self.create_delivery_note()
        first_delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        first_delivery_note.picking_ids = picking
        first_delivery_note.action_confirm()
        self.assertEqual(len(first_delivery_note.line_ids), 4)
        self.assertEqual(first_delivery_note.state, 'confirm')
        self.assertEqual(first_delivery_note.invoice_status, 'to invoice')

        sales_order.action_invoice_create(final=False)
        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, 'no')

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 2)

        partial_invoice = invoices[0]
        self.assertEqual(len(partial_invoice.invoice_line_ids), 5)
        self.assertEqual(partial_invoice.delivery_note_ids,
                         first_delivery_note)

        self.assertEqual(len(first_delivery_note.line_ids), 4)
        self.assertEqual(first_delivery_note.state, 'invoiced')
        self.assertEqual(first_delivery_note.invoice_status, 'invoiced')
        self.assertEqual(first_delivery_note.invoice_ids, partial_invoice)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        backorder = StockPicking.search([('backorder_id', '=', picking.id)])
        self.assertEqual(len(backorder), 1)
        self.assertEqual(len(backorder.move_lines), 3)

        backorder.move_lines[0].quantity_done = 1
        backorder.move_lines[1].quantity_done = 5
        backorder.move_lines[2].quantity_done = 2

        result = backorder.button_validate()
        self.assertIsNone(result)

        second_delivery_note = self.create_delivery_note()
        second_delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        second_delivery_note.picking_ids = backorder
        second_delivery_note.action_confirm()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, 'confirm')
        self.assertEqual(second_delivery_note.invoice_status, 'to invoice')

        #
        # Linea 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 1)
        self.assertEqual(order_line.qty_invoiced, 2)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 2)

        delivery_note_line = first_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = partial_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Linea 2
        #
        order_line = sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 2)

        delivery_note_line = first_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = partial_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Linea 3
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 5)
        self.assertEqual(order_line.qty_invoiced, 6)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 6)

        delivery_note_line = first_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 6)

        invoice_line = partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 6)

        #
        # Linea 4
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 2)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 3)

        delivery_note_line = first_delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Linea 5 (DdT in fattura)
        #
        invoice_line = partial_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_delivery_note.action_invoice()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, 'invoiced')
        self.assertEqual(second_delivery_note.invoice_status, 'invoiced')

        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, 'invoiced')

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 3)

        final_invoice = invoices[0]
        self.assertEqual(len(final_invoice.invoice_line_ids), 5)
        self.assertEqual(final_invoice.delivery_note_ids, second_delivery_note)

        self.assertEqual(second_delivery_note.invoice_ids, final_invoice)

        #
        # Linea ordine 1
        # Linea fattura 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 1)

        delivery_note_line = second_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Linea ordine 3
        # Linea fattura 2
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 5)

        delivery_note_line = second_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 5)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 5)

        #
        # Linea ordine 4
        # Linea fattura 3
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 2)

        delivery_note_line = second_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Linea ordine 5 (Downpayment)
        # Linea fattura 4
        #
        order_line = sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped('line_ids') \
            .filtered(lambda l: l.sale_line_id == order_line)

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Linea fattura 5 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, second_delivery_note)

    # ⇒ "Ordini multipli: fatturazione completa"
    def test_complete_invoicing_multiple_so(self):
        #
        #     SO ┐
        #        └ Picking ┐
        #                  ├ DdT
        #        ┌ Picking ┘
        #     SO ┘
        #

        first_sales_order = self.create_sales_order([
            self.desk_combination_line,
            self.customizable_desk_line,
            self.right_corner_desk_line
        ])
        self.assertEqual(len(first_sales_order.order_line), 3)

        first_sales_order.action_confirm()
        self.add_downpayment_line(first_sales_order, 'percentage', 10)
        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, 'no')

        downpayment_order_line = first_sales_order.order_line[3]
        self.assertEqual(downpayment_order_line.invoice_status, 'to invoice')
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = first_sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        first_picking = first_sales_order.picking_ids
        self.assertEqual(len(first_picking), 1)
        self.assertEqual(len(first_picking.move_lines), 3)

        first_picking.move_lines[0].quantity_done = 1
        first_picking.move_lines[1].quantity_done = 3
        first_picking.move_lines[2].quantity_done = 2

        result = first_picking.button_validate()
        self.assertIsNone(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_sales_order = self.create_sales_order([
            self.large_cabinet_line,
            self.storage_box_line,
            self.large_desk_line
        ])
        self.assertEqual(len(second_sales_order.order_line), 3)

        second_sales_order.action_confirm()
        self.assertEqual(second_sales_order.invoice_status, 'no')

        second_picking = second_sales_order.picking_ids
        self.assertEqual(len(second_picking), 1)
        self.assertEqual(len(second_picking.move_lines), 3)

        second_picking.move_lines[0].quantity_done = 11
        second_picking.move_lines[1].quantity_done = 5
        second_picking.move_lines[2].quantity_done = 1

        result = second_picking.button_validate()
        self.assertIsNone(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        pickings = first_picking | second_picking
        delivery_note = self.create_delivery_note()
        delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        delivery_note.picking_ids = pickings
        delivery_note.action_confirm()
        self.assertEqual(len(delivery_note.line_ids), 6)
        self.assertEqual(delivery_note.state, 'confirm')
        self.assertEqual(delivery_note.invoice_status, 'to invoice')

        delivery_note.action_invoice()
        self.assertEqual(len(delivery_note.line_ids), 6)
        self.assertEqual(delivery_note.state, 'invoiced')
        self.assertEqual(delivery_note.invoice_status, 'invoiced')

        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, 'invoiced')

        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, 'invoiced')

        sales_orders = first_sales_order | second_sales_order

        invoices = sales_orders.mapped('invoice_ids')
        self.assertEqual(len(invoices), 2)

        final_invoice = invoices[0]
        self.assertEqual(len(final_invoice.invoice_line_ids), 8)
        self.assertEqual(final_invoice.delivery_note_ids, delivery_note)

        self.assertEqual(delivery_note.invoice_ids, final_invoice)

        #
        # Ordine 1 - Linea 1
        # Linea fattura 1
        #
        order_line = first_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 2
        # Linea fattura 2
        #
        order_line = first_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 3)

        delivery_note_line = delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Ordine 1 - Linea 3
        # Linea fattura 3
        #
        order_line = first_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 2)

        delivery_note_line = delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine 1 - Linea 4 (Downpayment)
        # Linea fattura 4
        #
        order_line = first_sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids \
            .filtered(lambda l: l.sale_line_id == order_line)

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Ordine 2 - Linea 1
        # Linea fattura 5
        #
        order_line = second_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 11)

        delivery_note_line = delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 11)

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 11)

        #
        # Ordine 2 - Linea 2
        # Linea fattura 6
        #
        order_line = second_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 5)

        delivery_note_line = delivery_note.line_ids[4]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 5)

        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 5)

        #
        # Ordine 2 - Linea 3
        # Linea fattura 7
        #
        order_line = second_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = delivery_note.line_ids[5]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[6]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Linea fattura 8 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[7]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, delivery_note)

    # ⇒ "Ordini multipli: fatturazione parziale"
    def test_partial_invoicing_multiple_so(self):
        #
        #        ┌ Picking ──────┐
        #     SO ┤               ├ DdT
        #        │     ┌ Picking ┘
        #        │  SO ┤
        #        │     └ Picking ┐
        #        │               ├ DdT
        #        └ Picking ──────┘
        #

        StockPicking = self.env['stock.picking']
        StockBackorderConfirmationWizard = self.env[
            'stock.backorder.confirmation']

        first_sales_order = self.create_sales_order([
            self.desk_combination_line,
            self.right_corner_desk_line,
            self.large_desk_line
        ])
        self.assertEqual(len(first_sales_order.order_line), 3)

        first_sales_order.action_confirm()
        self.add_downpayment_line(first_sales_order, 'percentage', 10)
        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, 'no')

        downpayment_order_line = first_sales_order.order_line[3]
        self.assertEqual(downpayment_order_line.invoice_status, 'to invoice')
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = first_sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        first_picking = first_sales_order.picking_ids
        self.assertEqual(len(first_picking), 1)
        self.assertEqual(len(first_picking.move_lines), 3)

        first_picking.move_lines[0].quantity_done = 1
        first_picking.move_lines[1].quantity_done = 1  # 2
        first_picking.move_lines[2].quantity_done = 1

        wizard = StockBackorderConfirmationWizard.create({
            'pick_ids': [(4, first_picking.id)]
        })
        wizard.process()

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_sales_order = self.create_sales_order([
            self.customizable_desk_line,
            self.large_cabinet_line,
            self.storage_box_line
        ])
        self.assertEqual(len(second_sales_order.order_line), 3)

        second_sales_order.action_confirm()
        self.assertEqual(second_sales_order.invoice_status, 'no')

        second_picking = second_sales_order.picking_ids
        self.assertEqual(len(second_picking), 1)
        self.assertEqual(len(second_picking.move_lines), 3)

        second_picking.move_lines[0].quantity_done = 3
        second_picking.move_lines[1].quantity_done = 3  # 11
        second_picking.move_lines[2].quantity_done = 3  # 5

        wizard = StockBackorderConfirmationWizard.create({
            'pick_ids': [(4, second_picking.id)]
        })
        wizard.process()

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        pickings = first_picking | second_picking
        first_delivery_note = self.create_delivery_note()
        first_delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        first_delivery_note.picking_ids = pickings
        first_delivery_note.action_confirm()
        self.assertEqual(len(first_delivery_note.line_ids), 6)
        self.assertEqual(first_delivery_note.state, 'confirm')
        self.assertEqual(first_delivery_note.invoice_status, 'to invoice')

        first_sales_order.action_invoice_create(final=False)
        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, 'no')

        second_sales_order.action_invoice_create(final=False)
        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, 'no')

        sales_orders = first_sales_order | second_sales_order

        invoices = sales_orders.mapped('invoice_ids')
        self.assertEqual(len(invoices), 3)

        first_partial_invoice = invoices[0]
        self.assertEqual(len(first_partial_invoice.invoice_line_ids), 4)
        self.assertEqual(first_partial_invoice.delivery_note_ids,
                         first_delivery_note)

        second_partial_invoice = invoices[2]
        self.assertEqual(len(second_partial_invoice.invoice_line_ids), 4)
        self.assertEqual(second_partial_invoice.delivery_note_ids,
                         first_delivery_note)

        self.assertEqual(len(first_delivery_note.line_ids), 6)
        #
        # TODO: self.assertEqual(first_delivery_note.state, 'invoiced')?
        #
        self.assertEqual(len(first_delivery_note.invoice_ids), 2)
        self.assertEqual(first_delivery_note.invoice_ids[1],
                         first_partial_invoice)
        self.assertEqual(first_delivery_note.invoice_ids[0],
                         second_partial_invoice)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        first_backorder = \
            StockPicking.search([('backorder_id', '=', first_picking.id)])
        self.assertEqual(len(first_backorder), 1)
        self.assertEqual(len(first_backorder.move_lines), 1)

        first_backorder.move_lines[0].quantity_done = 1

        result = first_backorder.button_validate()
        self.assertIsNone(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_backorder = \
            StockPicking.search([('backorder_id', '=', second_picking.id)])
        self.assertEqual(len(second_backorder), 1)
        self.assertEqual(len(second_backorder.move_lines), 2)

        second_backorder.move_lines[0].quantity_done = 8
        second_backorder.move_lines[1].quantity_done = 2

        result = second_backorder.button_validate()
        self.assertIsNone(result)

        backorders = first_backorder | second_backorder
        second_delivery_note = self.create_delivery_note()
        second_delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        second_delivery_note.picking_ids = backorders
        second_delivery_note.action_confirm()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, 'confirm')
        self.assertEqual(second_delivery_note.invoice_status, 'to invoice')

        #
        # Ordine 1 - Linea 1
        # Fattura 1 - Linea 1
        #
        order_line = first_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = first_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = first_partial_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 2
        # Fattura 1 - Linea 2
        #
        order_line = first_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 1)
        self.assertEqual(order_line.qty_invoiced, 1)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 1)

        delivery_note_line = first_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = first_partial_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 3
        # Fattura 1 - Linea 3
        #
        order_line = first_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 1)

        delivery_note_line = first_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = first_partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Fattura 1 - Linea 4 (DdT in fattura)
        #
        invoice_line = first_partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # Ordine 2 - Linea 1
        # Fattura 2 - Linea 1
        #
        order_line = second_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity_done, 3)

        delivery_note_line = first_delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = second_partial_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Ordine 2 - Linea 2
        # Fattura 2 - Linea 2
        #
        order_line = second_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 8)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 3)

        delivery_note_line = first_delivery_note.line_ids[4]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = second_partial_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Ordine 2 - Linea 3
        # Fattura 2 - Linea 3
        #
        order_line = second_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'to invoice')
        self.assertEqual(order_line.qty_to_invoice, 2)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity_done, 3)

        delivery_note_line = first_delivery_note.line_ids[5]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = second_partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Fattura 2 - Linea 4 (DdT in fattura)
        #
        invoice_line = second_partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_delivery_note.action_invoice()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, 'invoiced')
        self.assertEqual(second_delivery_note.invoice_status, 'invoiced')

        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, 'invoiced')

        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, 'invoiced')

        invoices = sales_orders.mapped('invoice_ids')
        self.assertEqual(len(invoices), 4)

        final_invoice = invoices[1]
        self.assertEqual(len(final_invoice.invoice_line_ids), 5)
        self.assertEqual(final_invoice.delivery_note_ids, second_delivery_note)

        self.assertEqual(second_delivery_note.invoice_ids, final_invoice)

        #
        # Ordine 1 - Linea 2
        # Fattura 3 - Linea 1
        #
        order_line = first_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 1)

        delivery_note_line = second_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 4 (Downpayment)
        # Fattura 3 - Linea 2
        #
        order_line = first_sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped('line_ids') \
            .filtered(lambda l: l.sale_line_id == order_line)

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Ordine 2 - Linea 2
        # Fattura 3 - Linea 3
        #
        order_line = second_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 8)

        delivery_note_line = second_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 8)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 8)

        #
        # Ordine 2 - Linea 3
        # Fattura 3 - Linea 4
        #
        order_line = second_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, 'invoiced')
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity_done, 2)

        delivery_note_line = second_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, 'invoiced')
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Fattura 3 - Linea 5 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.display_type, 'line_note')
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, second_delivery_note)
