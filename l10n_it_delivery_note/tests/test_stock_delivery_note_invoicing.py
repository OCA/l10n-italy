from datetime import datetime, timedelta

from odoo.tests import Form

from ..models.stock_delivery_note import DATE_FORMAT
from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNoteInvoicingTest(StockDeliveryNoteCommon):
    # ⇒ "Ordine singolo: fatturazione completa"
    def test_complete_invoicing_single_so(self):
        #
        #     SO ┐         ┌ DdT
        #        └ Picking ┘
        #

        sales_order = self.create_sales_order(
            [
                self.desk_combination_line,
                self.right_corner_desk_line,
                self.large_cabinet_line,
                self.large_desk_line,
            ]
        )
        self.assertEqual(len(sales_order.order_line), 4)

        sales_order.action_confirm()
        self.add_downpayment_line(sales_order, "percentage", 10)
        self.assertEqual(len(sales_order.order_line), 6)
        self.assertEqual(sales_order.invoice_status, "no")

        downpayment_order_line = sales_order.order_line[5]
        self.assertEqual(downpayment_order_line.invoice_status, "invoiced")
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        picking = sales_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_ids), 4)

        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1
        picking.move_ids[1].quantity = 2
        picking.move_ids[2].quantity = 11
        picking.move_ids[3].quantity = 1

        result = picking.button_validate()
        self.assertTrue(result)

        delivery_note = self.create_delivery_note()
        delivery_note.transport_datetime = datetime.now() + timedelta(days=1, hours=3)
        delivery_note.picking_ids = picking
        delivery_note.action_confirm()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, "confirm")
        self.assertEqual(delivery_note.invoice_status, "to invoice")

        delivery_note.action_invoice()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, "invoiced")
        self.assertEqual(delivery_note.invoice_status, "invoiced")

        self.assertEqual(len(sales_order.order_line), 6)
        self.assertEqual(sales_order.invoice_status, "invoiced")

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 2)

        final_invoice = invoices[0]
        # in sale.advance.payment.inv the method create_invoices uses the field
        # deduct_down_payments (default True) that includes selection lines:
        # so 4 product lines, 1 ddt note, 1 down_payment and 1 selection line
        self.assertEqual(len(final_invoice.invoice_line_ids), 7)
        self.assertEqual(final_invoice.delivery_note_ids, delivery_note)

        self.assertEqual(delivery_note.invoice_ids, final_invoice)

        #
        # Ordine - Linea 1
        # Fattura - Linea 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine - Linea 2
        # Fattura - Linea 2
        #
        order_line = sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 2)

        delivery_note_line = delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine - Linea 3
        # Fattura - Linea 3
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 11)

        delivery_note_line = delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 11)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 11)

        #
        # Ordine - Linea 4
        # Fattura - Linea 4
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine - Linea 5
        # Fattura - Linea 5 section (Downpayment)
        # Fattura - Linea 6 (Downpayment)
        #
        order_line = sales_order.order_line[5]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids.filtered(
            lambda note_line: note_line.sale_line_id == order_line
        )

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.display_type, "line_section")
        self.assertEqual(invoice_line.name, "Down Payments")

        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Fattura - Linea 7 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[6]
        self.assertEqual(invoice_line.display_type, "line_note")
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

        StockPicking = self.env["stock.picking"]

        sales_order = self.create_sales_order(
            [
                self.customizable_desk_line,
                self.right_corner_desk_line,
                self.large_cabinet_line,
                self.storage_box_line,
            ]
        )
        self.assertEqual(len(sales_order.order_line), 4)

        sales_order.action_confirm()
        self.add_downpayment_line(sales_order, "percentage", 10)
        self.assertEqual(len(sales_order.order_line), 6)
        self.assertEqual(sales_order.invoice_status, "no")

        downpayment_order_line = sales_order.order_line[5]
        self.assertEqual(downpayment_order_line.invoice_status, "invoiced")
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        picking = sales_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_ids), 4)

        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 2  # 3
        picking.move_ids[1].quantity = 2
        picking.move_ids[2].quantity = 6  # 11
        picking.move_ids[3].quantity = 3  # 5

        result = picking.button_validate()
        self.assertTrue(result)

        wizard = Form.from_action(self.env, result).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()

        first_delivery_note = self.create_delivery_note()
        first_delivery_note.transport_datetime = datetime.now() + timedelta(
            days=1, hours=3
        )
        first_delivery_note.picking_ids = picking
        first_delivery_note.action_confirm()
        self.assertEqual(len(first_delivery_note.line_ids), 4)
        self.assertEqual(first_delivery_note.state, "confirm")
        self.assertEqual(first_delivery_note.invoice_status, "to invoice")

        sales_order._create_invoices()

        self.assertEqual(len(sales_order.order_line), 6)
        self.assertEqual(sales_order.invoice_status, "no")

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 2)

        partial_invoice = invoices[0]
        self.assertEqual(len(partial_invoice.invoice_line_ids), 5)
        self.assertEqual(partial_invoice.delivery_note_ids, first_delivery_note)

        self.assertEqual(len(first_delivery_note.line_ids), 4)
        self.assertEqual(first_delivery_note.state, "invoiced")
        self.assertEqual(first_delivery_note.invoice_status, "invoiced")
        self.assertEqual(first_delivery_note.invoice_ids, partial_invoice)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(backorder), 1)
        self.assertEqual(len(backorder.move_ids), 3)

        backorder.move_ids.quantity = False
        backorder.move_ids[0].quantity = 1
        backorder.move_ids[1].quantity = 5
        backorder.move_ids[2].quantity = 2

        result = backorder.button_validate()
        self.assertTrue(result)

        second_delivery_note = self.create_delivery_note()
        second_delivery_note.transport_datetime = datetime.now() + timedelta(
            days=1, hours=3
        )
        second_delivery_note.picking_ids = backorder
        second_delivery_note.action_confirm()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, "confirm")
        self.assertEqual(second_delivery_note.invoice_status, "to invoice")

        #
        # Ordine - Linea 1
        # Fattura - Linea 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 1)
        self.assertEqual(order_line.qty_invoiced, 2)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 2)

        delivery_note_line = first_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = partial_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine - Linea 2
        # Fattura - Linea 2
        #
        order_line = sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 2)

        delivery_note_line = first_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = partial_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine - Linea 3
        # Fattura - Linea 3
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 5)
        self.assertEqual(order_line.qty_invoiced, 6)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 6)

        delivery_note_line = first_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 6)

        invoice_line = partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 6)

        #
        # Ordine - Linea 4
        # Fattura - Linea 4
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 2)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 3)

        delivery_note_line = first_delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Fattura - Linea 5 (DdT in fattura)
        #
        invoice_line = partial_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.display_type, "line_note")
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_delivery_note.action_invoice()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, "invoiced")
        self.assertEqual(second_delivery_note.invoice_status, "invoiced")

        self.assertEqual(len(sales_order.order_line), 6)
        self.assertEqual(sales_order.invoice_status, "invoiced")

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 3)

        final_invoice = invoices[1]
        self.assertEqual(len(final_invoice.invoice_line_ids), 6)
        self.assertEqual(final_invoice.delivery_note_ids, second_delivery_note)

        self.assertEqual(second_delivery_note.invoice_ids, final_invoice)

        #
        # Ordine - Linea 1
        # Fattura - Linea 1
        #
        order_line = sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 1)

        delivery_note_line = second_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine - Linea 3
        # Fattura - Linea 2
        #
        order_line = sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 5)

        delivery_note_line = second_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 5)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 5)

        #
        # Ordine - Linea 4
        # Fattura - Linea 3
        #
        order_line = sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 2)

        delivery_note_line = second_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine - Linea 5 (Downpayment)
        # Fattura - Linea 4 section (Downpayment)
        # Fattura - Linea 5 (Downpayment)
        #
        order_line = sales_order.order_line[5]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped("line_ids").filtered(
            lambda note_line: note_line.sale_line_id == order_line
        )

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, "line_section")
        self.assertEqual(invoice_line.name, "Down Payments")

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Fattura - Linea 6 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.display_type, "line_note")
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

        first_sales_order = self.create_sales_order(
            [
                self.desk_combination_line,
                self.customizable_desk_line,
                self.right_corner_desk_line,
            ]
        )
        self.assertEqual(len(first_sales_order.order_line), 3)

        first_sales_order.action_confirm()
        self.add_downpayment_line(first_sales_order, "percentage", 10)
        self.assertEqual(len(first_sales_order.order_line), 5)
        self.assertEqual(first_sales_order.invoice_status, "no")

        downpayment_order_line = first_sales_order.order_line[4]
        self.assertEqual(downpayment_order_line.invoice_status, "invoiced")
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = first_sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        first_picking = first_sales_order.picking_ids
        self.assertEqual(len(first_picking), 1)
        self.assertEqual(len(first_picking.move_ids), 3)

        first_picking.move_ids.quantity = False
        first_picking.move_ids[0].quantity = 1
        first_picking.move_ids[1].quantity = 3
        first_picking.move_ids[2].quantity = 2

        result = first_picking.button_validate()
        self.assertTrue(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_sales_order = self.create_sales_order(
            [self.large_cabinet_line, self.storage_box_line, self.large_desk_line]
        )
        self.assertEqual(len(second_sales_order.order_line), 3)

        second_sales_order.action_confirm()
        self.assertEqual(second_sales_order.invoice_status, "no")

        second_picking = second_sales_order.picking_ids
        self.assertEqual(len(second_picking), 1)
        self.assertEqual(len(second_picking.move_ids), 3)

        second_picking.move_ids.quantity = False
        second_picking.move_ids[0].quantity = 11
        second_picking.move_ids[1].quantity = 5
        second_picking.move_ids[2].quantity = 1

        result = second_picking.button_validate()
        self.assertTrue(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        pickings = first_picking | second_picking
        delivery_note = self.create_delivery_note()
        delivery_note.transport_datetime = datetime.now() + timedelta(days=1, hours=3)
        delivery_note.picking_ids = pickings
        delivery_note.action_confirm()
        self.assertEqual(len(delivery_note.line_ids), 6)
        self.assertEqual(delivery_note.state, "confirm")
        self.assertEqual(delivery_note.invoice_status, "to invoice")

        delivery_note.action_invoice()
        self.assertEqual(len(delivery_note.line_ids), 6)
        self.assertEqual(delivery_note.state, "invoiced")
        self.assertEqual(delivery_note.invoice_status, "invoiced")

        self.assertEqual(len(first_sales_order.order_line), 5)
        self.assertEqual(first_sales_order.invoice_status, "invoiced")

        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, "invoiced")

        sales_orders = first_sales_order | second_sales_order

        invoices = sales_orders.mapped("invoice_ids")
        self.assertEqual(len(invoices), 2)

        final_invoice = invoices[0]
        self.assertEqual(len(final_invoice.invoice_line_ids), 9)
        self.assertEqual(final_invoice.delivery_note_ids, delivery_note)

        self.assertEqual(delivery_note.invoice_ids, final_invoice)

        #
        # Ordine 1 - Linea 1
        # Fattura - Linea 1
        #
        order_line = first_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 2
        # Fattura - Linea 2
        #
        order_line = first_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 3)

        delivery_note_line = delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Ordine 1 - Linea 3
        # Fattura - Linea 3
        #
        order_line = first_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 2)

        delivery_note_line = delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Ordine 1 - Linea 4 (Downpayment)
        # Fattura - Linea 4 section (Downpayment)
        # Fattura - Linea 5 (Downpayment)
        #
        order_line = first_sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids.filtered(
            lambda note_line: note_line.sale_line_id == order_line
        )

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, "line_section")
        self.assertEqual(invoice_line.name, "Down Payments")

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Ordine 2 - Linea 1
        # Fattura - Linea 6
        #
        order_line = second_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 11)

        delivery_note_line = delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 11)

        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 11)

        #
        # Ordine 2 - Linea 2
        # Fattura - Linea 7
        #
        order_line = second_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 5)

        delivery_note_line = delivery_note.line_ids[4]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 5)

        invoice_line = final_invoice.invoice_line_ids[6]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 5)

        #
        # Ordine 2 - Linea 3
        # Fattura - Linea 8
        #
        order_line = second_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = delivery_note.line_ids[5]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[7]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Fattura - Linea 9 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[8]
        self.assertEqual(invoice_line.display_type, "line_note")
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

        StockPicking = self.env["stock.picking"]

        first_sales_order = self.create_sales_order(
            [
                self.desk_combination_line,
                self.right_corner_desk_line,
                self.large_desk_line,
            ]
        )
        self.assertEqual(len(first_sales_order.order_line), 3)

        first_sales_order.action_confirm()
        self.add_downpayment_line(first_sales_order, "percentage", 10)
        self.assertEqual(len(first_sales_order.order_line), 5)
        self.assertEqual(first_sales_order.invoice_status, "no")

        downpayment_order_line = first_sales_order.order_line[4]
        self.assertEqual(downpayment_order_line.invoice_status, "invoiced")
        self.assertEqual(downpayment_order_line.qty_to_invoice, -1)
        self.assertEqual(downpayment_order_line.qty_invoiced, 1)

        downpayment_invoice = first_sales_order.invoice_ids
        self.assertEqual(len(downpayment_invoice), 1)

        downpayment_invoice_line = downpayment_invoice.invoice_line_ids
        self.assertEqual(len(downpayment_invoice_line), 1)
        self.assertEqual(downpayment_invoice_line.quantity, 1)

        first_picking = first_sales_order.picking_ids
        self.assertEqual(len(first_picking), 1)
        self.assertEqual(len(first_picking.move_ids), 3)

        first_picking.move_ids.quantity = False
        first_picking.move_ids[0].quantity = 1
        first_picking.move_ids[1].quantity = 1  # 2
        first_picking.move_ids[2].quantity = 1

        result = first_picking.button_validate()
        self.assertTrue(result)

        wizard = Form.from_action(self.env, result).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_sales_order = self.create_sales_order(
            [
                self.customizable_desk_line,
                self.large_cabinet_line,
                self.storage_box_line,
            ]
        )
        self.assertEqual(len(second_sales_order.order_line), 3)

        second_sales_order.action_confirm()
        self.assertEqual(second_sales_order.invoice_status, "no")

        second_picking = second_sales_order.picking_ids
        self.assertEqual(len(second_picking), 1)
        self.assertEqual(len(second_picking.move_ids), 3)

        second_picking.move_ids.quantity = False
        second_picking.move_ids[0].quantity = 3
        second_picking.move_ids[1].quantity = 3  # 11
        second_picking.move_ids[2].quantity = 3  # 5

        result = second_picking.button_validate()
        self.assertTrue(result)

        wizard = Form.from_action(self.env, result).save()
        self.assertEqual(wizard._name, "stock.backorder.confirmation")
        wizard.process()

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        pickings = first_picking | second_picking
        first_delivery_note = self.create_delivery_note()
        first_delivery_note.transport_datetime = datetime.now() + timedelta(
            days=1, hours=3
        )
        first_delivery_note.picking_ids = pickings
        first_delivery_note.action_confirm()
        self.assertEqual(len(first_delivery_note.line_ids), 6)
        self.assertEqual(first_delivery_note.state, "confirm")
        self.assertEqual(first_delivery_note.invoice_status, "to invoice")

        first_sales_order._create_invoices()
        self.assertEqual(len(first_sales_order.order_line), 5)
        self.assertEqual(first_sales_order.invoice_status, "no")

        second_sales_order._create_invoices()
        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, "no")

        sales_orders = first_sales_order | second_sales_order

        invoices = sales_orders.mapped("invoice_ids")
        self.assertEqual(len(invoices), 3)

        first_partial_invoice = invoices[0]
        self.assertEqual(len(first_partial_invoice.invoice_line_ids), 4)
        self.assertEqual(first_partial_invoice.delivery_note_ids, first_delivery_note)

        second_partial_invoice = invoices[2]
        self.assertEqual(len(second_partial_invoice.invoice_line_ids), 4)
        self.assertEqual(second_partial_invoice.delivery_note_ids, first_delivery_note)

        self.assertEqual(len(first_delivery_note.line_ids), 6)
        self.assertEqual(first_delivery_note.state, "invoiced")
        self.assertEqual(len(first_delivery_note.invoice_ids), 2)
        self.assertEqual(first_delivery_note.invoice_ids[0], first_partial_invoice)
        self.assertEqual(first_delivery_note.invoice_ids[1], second_partial_invoice)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        first_backorder = StockPicking.search([("backorder_id", "=", first_picking.id)])
        self.assertEqual(len(first_backorder), 1)
        self.assertEqual(len(first_backorder.move_ids), 1)

        first_backorder.move_ids.quantity = False
        first_backorder.move_ids[0].quantity = 1

        result = first_backorder.button_validate()
        self.assertTrue(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_backorder = StockPicking.search(
            [("backorder_id", "=", second_picking.id)]
        )
        self.assertEqual(len(second_backorder), 1)
        self.assertEqual(len(second_backorder.move_ids), 2)

        second_backorder.move_ids.quantity = False
        second_backorder.move_ids[0].quantity = 8
        second_backorder.move_ids[1].quantity = 2

        result = second_backorder.button_validate()
        self.assertTrue(result)

        backorders = first_backorder | second_backorder
        second_delivery_note = self.create_delivery_note()
        second_delivery_note.transport_datetime = datetime.now() + timedelta(
            days=1, hours=3
        )
        second_delivery_note.picking_ids = backorders
        second_delivery_note.action_confirm()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, "confirm")
        self.assertEqual(second_delivery_note.invoice_status, "to invoice")

        #
        # Ordine 1 - Linea 1
        # Fattura 1 - Linea 1
        #
        order_line = first_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = first_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
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
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 1)
        self.assertEqual(order_line.qty_invoiced, 1)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 1)

        delivery_note_line = first_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
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
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 1)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 1)

        delivery_note_line = first_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = first_partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Fattura 1 - Linea 4 (DdT in fattura)
        #
        invoice_line = first_partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, "line_note")
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # Ordine 2 - Linea 1
        # Fattura 2 - Linea 1
        #
        order_line = second_sales_order.order_line[0]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 3)

        move = order_line.move_ids
        self.assertEqual(len(move), 1)
        self.assertEqual(move.quantity, 3)

        delivery_note_line = first_delivery_note.line_ids[3]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
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
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 8)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 3)

        delivery_note_line = first_delivery_note.line_ids[4]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
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
        self.assertEqual(order_line.invoice_status, "to invoice")
        self.assertEqual(order_line.qty_to_invoice, 2)
        self.assertEqual(order_line.qty_invoiced, 3)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[0].quantity, 3)

        delivery_note_line = first_delivery_note.line_ids[5]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 3)

        invoice_line = second_partial_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 3)

        #
        # Fattura 2 - Linea 4 (DdT in fattura)
        #
        invoice_line = second_partial_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.display_type, "line_note")
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, first_delivery_note)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_delivery_note.action_invoice()
        self.assertEqual(len(second_delivery_note.line_ids), 3)
        self.assertEqual(second_delivery_note.state, "invoiced")
        self.assertEqual(second_delivery_note.invoice_status, "invoiced")

        self.assertEqual(len(first_sales_order.order_line), 5)
        self.assertEqual(first_sales_order.invoice_status, "invoiced")

        self.assertEqual(len(second_sales_order.order_line), 3)
        self.assertEqual(second_sales_order.invoice_status, "invoiced")

        invoices = sales_orders.mapped("invoice_ids")
        self.assertEqual(len(invoices), 4)

        final_invoice = invoices[1]
        self.assertEqual(len(final_invoice.invoice_line_ids), 6)
        self.assertEqual(final_invoice.delivery_note_ids, second_delivery_note)

        self.assertEqual(second_delivery_note.invoice_ids, final_invoice)

        #
        # Ordine 1 - Linea 2
        # Fattura 3 - Linea 1
        #
        order_line = first_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 2)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 1)

        delivery_note_line = second_delivery_note.line_ids[0]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 1)

        invoice_line = final_invoice.invoice_line_ids[0]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 1)

        #
        # Ordine 1 - Linea 4 (Downpayment)
        # Fattura 3 - Linea 2 section (Downpayment)
        # Fattura 3 - Linea 3 (Downpayment)
        #
        order_line = first_sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped("line_ids").filtered(
            lambda note_line: note_line.sale_line_id == order_line
        )

        self.assertEqual(len(delivery_note_line), 0)

        invoice_line = final_invoice.invoice_line_ids[1]
        self.assertEqual(invoice_line.display_type, "line_section")
        self.assertEqual(invoice_line.name, "Down Payments")

        invoice_line = final_invoice.invoice_line_ids[2]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, -1)

        #
        # Ordine 2 - Linea 2
        # Fattura 3 - Linea 4
        #
        order_line = second_sales_order.order_line[1]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 11)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 8)

        delivery_note_line = second_delivery_note.line_ids[1]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 8)

        invoice_line = final_invoice.invoice_line_ids[3]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 8)

        #
        # Ordine 2 - Linea 3
        # Fattura 3 - Linea 5
        #
        order_line = second_sales_order.order_line[2]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 5)

        moves = order_line.move_ids
        self.assertEqual(len(moves), 2)
        self.assertEqual(moves[1].quantity, 2)

        delivery_note_line = second_delivery_note.line_ids[2]
        self.assertEqual(delivery_note_line.invoice_status, "invoiced")
        self.assertEqual(delivery_note_line.sale_line_id, order_line)
        self.assertEqual(delivery_note_line.product_qty, 2)

        invoice_line = final_invoice.invoice_line_ids[4]
        self.assertEqual(invoice_line.sale_line_ids, order_line)
        self.assertEqual(invoice_line.quantity, 2)

        #
        # Fattura 3 - Linea 6 (DdT in fattura)
        #
        invoice_line = final_invoice.invoice_line_ids[5]
        self.assertEqual(invoice_line.display_type, "line_note")
        self.assertEqual(invoice_line.quantity, 0)
        self.assertEqual(invoice_line.delivery_note_id, second_delivery_note)

    def test_delivery_note_to_draft_from_create(self):
        """
        Create delivery_note from picking with already invoiced sale order then validate
        and reset the status to draft.
        """
        sales_order = self.create_sales_order(
            [
                self.desk_combination_line,
            ]
        )
        sales_order.action_confirm()
        picking = sales_order.picking_ids
        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1
        picking.button_validate()
        sales_order._create_invoices()
        wizard = Form.from_action(
            self.env, picking.action_delivery_note_create()
        ).save()
        result = wizard.confirm()
        delivery_note = self.env["stock.delivery.note"].browse(result["res_id"])
        delivery_note.action_confirm()
        delivery_note.action_cancel()
        delivery_note.action_draft()
        self.assertEqual(delivery_note.invoice_status, "no")
        self.assertEqual(delivery_note.state, "draft")

    def test_invoicing_multiple_dn(self):
        StockPicking = self.env["stock.picking"]
        sales_order = self.create_sales_order(
            [
                self.right_corner_desk_line,  # 2
                self.desk_combination_line,  # 1
            ],
        )
        self.assertEqual(len(sales_order.order_line), 2)
        sales_order.action_confirm()
        self.assertEqual(len(sales_order.picking_ids), 1)
        picking = sales_order.picking_ids
        self.assertEqual(len(picking.move_ids), 2)

        # deliver only half of the first product
        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1
        res_dict = picking.button_validate()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.process()
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.confirm()
        self.assertTrue(picking.delivery_note_id)
        dn = picking.delivery_note_id
        self.assertEqual(dn.partner_id, self.recipient)
        dn.action_confirm()
        dn.action_done()
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_ids), 2)
        picking_backorder.move_ids[0].quantity = 1
        picking_backorder.move_ids[1].quantity = 1
        picking_backorder.button_validate()
        self.assertEqual(picking_backorder.state, "done")
        back_res_dict = picking_backorder.action_delivery_note_create()
        back_wizard = Form(
            self.env[(back_res_dict.get("res_model"))].with_context(
                **back_res_dict["context"]
            )
        ).save()
        back_wizard.confirm()
        self.assertTrue(picking_backorder.delivery_note_id)
        back_dn = picking_backorder.delivery_note_id
        self.assertEqual(back_dn.partner_id, self.recipient)
        back_dn.action_confirm()
        back_dn.action_done()
        sales_order._create_invoices()
        self.assertTrue(len(sales_order.invoice_ids), 1)
        invoice = sales_order.invoice_ids
        invoice.action_post()
        self.assertEqual(invoice.state, "posted")
        self.assertRecordValues(
            invoice.invoice_line_ids.sorted("sequence"),
            [
                {
                    "note_dn": True,
                    "delivery_note_id": dn.id,
                    "product_id": False,
                    "quantity": 0,
                },
                {
                    "note_dn": False,
                    "delivery_note_id": dn.id,
                    "product_id": self.right_corner_desk_line[2]["product_id"],
                    "quantity": 1,
                },
                {
                    "note_dn": True,
                    "delivery_note_id": back_dn.id,
                    "product_id": False,
                    "quantity": 0,
                },
                {
                    "note_dn": False,
                    "delivery_note_id": back_dn.id,
                    "product_id": self.right_corner_desk_line[2]["product_id"],
                    "quantity": 1,
                },
                {
                    "note_dn": False,
                    "delivery_note_id": back_dn.id,
                    "product_id": self.desk_combination_line[2]["product_id"],
                    "quantity": 1,
                },
            ],
        )
        self.assertEqual(dn.invoice_status, "invoiced")
        self.assertEqual(back_dn.invoice_status, "invoiced")
        self.assertIn(
            f'Delivery Note "{dn.name}" of {dn.date.strftime(DATE_FORMAT)}',
            invoice.invoice_line_ids.mapped("name"),
        )
        self.assertIn(
            f'Delivery Note "{back_dn.name}" of {back_dn.date.strftime(DATE_FORMAT)}',
            invoice.invoice_line_ids.mapped("name"),
        )

    def test_invoicing_multi_dn_multi_so_same_product(self):
        # SO 1
        so_1 = self.create_sales_order([self.right_corner_desk_line])  # qty 2
        so_1.action_confirm()

        picking = so_1.picking_ids
        picking.move_ids[0].quantity = 1
        res_dict = picking.button_validate()
        # create backorder
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.process()
        # create delivery note
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1 = picking.delivery_note_id
        self.assertTrue(dn_1)
        self.assertEqual(dn_1.partner_id, self.recipient)
        dn_1.action_confirm()
        dn_1.action_done()

        # partial invoice for SO 1
        so_1_line = so_1.order_line
        so_1._create_invoices()
        self.assertEqual(so_1_line.invoice_status, "no")
        self.assertEqual(so_1_line.qty_invoiced, 1)

        inv_1 = so_1.invoice_ids
        inv_1.action_post()
        self.assertEqual(len(inv_1.invoice_line_ids), 2)
        label_line, product_line = inv_1.invoice_line_ids.sorted("sequence")
        self.assertIn(dn_1.name, label_line.name)
        self.assertIn(dn_1.date.strftime(DATE_FORMAT), label_line.name)
        self.assertEqual(product_line.product_id, so_1_line.product_id)
        self.assertEqual(product_line.quantity, 1)

        # deliver backorder
        backorder_so_1 = picking.backorder_ids
        backorder_so_1.move_ids[0].quantity = 1
        backorder_so_1.button_validate()
        res_dict = backorder_so_1.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.confirm()
        dn_backorder = backorder_so_1.delivery_note_id
        self.assertTrue(dn_backorder)
        self.assertEqual(dn_backorder.partner_id, self.recipient)
        dn_backorder.action_confirm()
        dn_backorder.action_done()

        # SO 2 and full delivery
        so_2 = self.create_sales_order([self.right_corner_desk_line])  # qty 2
        so_2.action_confirm()
        picking = so_2.picking_ids
        picking.move_ids[0].quantity = 2
        picking.button_validate()
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.confirm()
        dn_2 = picking.delivery_note_id
        self.assertTrue(dn_2)
        self.assertEqual(dn_2.partner_id, self.recipient)
        dn_2.action_confirm()
        dn_2.action_done()

        # invoice backorder of so_1 and full so_2 together
        (so_1 | so_2)._create_invoices()
        inv_2 = so_2.invoice_ids
        inv_2.action_post()
        (
            label_so_1,
            product_line_1,
            label_so_2,
            product_line_2,
        ) = inv_2.invoice_line_ids.sorted("sequence")
        self.assertIn(dn_backorder.name, label_so_1.name)
        self.assertIn(dn_backorder.date.strftime(DATE_FORMAT), label_so_1.name)
        self.assertEqual(product_line_1.product_id, so_1_line.product_id)
        self.assertEqual(product_line_1.quantity, 1)
        self.assertIn(dn_2.name, label_so_2.name)
        self.assertIn(dn_2.date.strftime(DATE_FORMAT), label_so_2.name)
        self.assertEqual(product_line_2.product_id, so_2.order_line.product_id)
        self.assertEqual(product_line_2.quantity, 2)

    def test_multiple_dn_invoice_one(self):
        """Create multiple Delivery Notes for the same Sale Order,
        and invoice only one Delivery Note.
        Only the lines of the invoiced Delivery Note
        are present in the invoice.
        """
        # Order 2 products, but deliver only 1
        sales_order = self.create_sales_order(
            [
                self.right_corner_desk_line,  # 2
            ],
        )
        sales_order.action_confirm()
        picking = sales_order.picking_ids
        picking.move_ids.quantity = 1

        # Confirm the picking as-is: create backorder
        res_dict = picking.button_validate()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.process()

        # Create Delivery Note
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(**res_dict["context"])
        ).save()
        wizard.confirm()
        dn = picking.delivery_note_id
        dn.action_confirm()
        dn.action_done()

        # Create Delivery Note for backorder
        picking_backorder = self.env["stock.picking"].search(
            [("backorder_id", "=", picking.id)]
        )
        picking_backorder.move_ids.quantity = 1
        picking_backorder.button_validate()
        back_res_dict = picking_backorder.action_delivery_note_create()
        back_wizard = Form(
            self.env[(back_res_dict.get("res_model"))].with_context(
                **back_res_dict["context"]
            )
        ).save()
        back_wizard.confirm()
        back_dn = picking_backorder.delivery_note_id
        back_dn.action_confirm()
        back_dn.action_done()

        dn.action_invoice()
        invoice = sales_order.invoice_ids
        invoice.action_post()
        self.assertRecordValues(
            invoice.invoice_line_ids.sorted("sequence"),
            [
                {
                    "note_dn": True,
                    "delivery_note_id": dn.id,
                    "product_id": False,
                    "quantity": 0,
                },
                {
                    "note_dn": False,
                    "delivery_note_id": dn.id,
                    "product_id": self.right_corner_desk_line[2]["product_id"],
                    "quantity": 1,
                },
            ],
        )
        self.assertEqual(dn.invoice_status, "invoiced")
        self.assertEqual(back_dn.invoice_status, "to invoice")
