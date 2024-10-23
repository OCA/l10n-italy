from datetime import datetime, timedelta

from odoo.tests import new_test_user
from odoo.tests.common import Form

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
        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, "no")

        downpayment_order_line = sales_order.order_line[4]
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
        self.assertEqual(len(picking.move_lines), 4)

        picking.move_lines[0].quantity_done = 1
        picking.move_lines[1].quantity_done = 2
        picking.move_lines[2].quantity_done = 11
        picking.move_lines[3].quantity_done = 1

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

        self.assertEqual(len(sales_order.order_line), 5)
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
        self.assertEqual(move.quantity_done, 1)

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
        self.assertEqual(move.quantity_done, 2)

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
        self.assertEqual(move.quantity_done, 11)

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
        self.assertEqual(move.quantity_done, 1)

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
        order_line = sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids.filtered(
            lambda l: l.sale_line_id == order_line
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
        self.assertEqual(len(sales_order.order_line), 5)
        self.assertEqual(sales_order.invoice_status, "no")

        downpayment_order_line = sales_order.order_line[4]
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
        self.assertEqual(len(picking.move_lines), 4)

        picking.move_lines[0].quantity_done = 2  # 3
        picking.move_lines[1].quantity_done = 2
        picking.move_lines[2].quantity_done = 6  # 11
        picking.move_lines[3].quantity_done = 3  # 5

        result = picking.button_validate()
        self.assertTrue(result)

        wizard = Form(
            self.env[(result.get("res_model"))].with_context(result["context"])
        ).save()
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

        self.assertEqual(len(sales_order.order_line), 5)
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
        self.assertEqual(len(backorder.move_lines), 3)

        backorder.move_lines[0].quantity_done = 1
        backorder.move_lines[1].quantity_done = 5
        backorder.move_lines[2].quantity_done = 2

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
        self.assertEqual(moves[0].quantity_done, 2)

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
        self.assertEqual(move.quantity_done, 2)

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
        self.assertEqual(moves[0].quantity_done, 6)

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
        self.assertEqual(moves[0].quantity_done, 3)

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

        self.assertEqual(len(sales_order.order_line), 5)
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
        self.assertEqual(moves[1].quantity_done, 1)

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
        self.assertEqual(moves[1].quantity_done, 5)

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
        self.assertEqual(moves[1].quantity_done, 2)

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
        order_line = sales_order.order_line[4]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped("line_ids").filtered(
            lambda l: l.sale_line_id == order_line
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

        # Activate advanced setting to allow more picking in one DN
        self.env["ir.config_parameter"].sudo().set_param(
            "l10n_it_delivery_note.group_use_advanced_delivery_notes", True
        )

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
        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, "no")

        downpayment_order_line = first_sales_order.order_line[3]
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
        self.assertEqual(len(first_picking.move_lines), 3)

        first_picking.move_lines[0].quantity_done = 1
        first_picking.move_lines[1].quantity_done = 3
        first_picking.move_lines[2].quantity_done = 2

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
        self.assertEqual(len(second_picking.move_lines), 3)

        second_picking.move_lines[0].quantity_done = 11
        second_picking.move_lines[1].quantity_done = 5
        second_picking.move_lines[2].quantity_done = 1

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

        self.assertEqual(len(first_sales_order.order_line), 4)
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
        self.assertEqual(move.quantity_done, 1)

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
        self.assertEqual(move.quantity_done, 3)

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
        self.assertEqual(move.quantity_done, 2)

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
        order_line = first_sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_note_line = delivery_note.line_ids.filtered(
            lambda l: l.sale_line_id == order_line
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
        self.assertEqual(move.quantity_done, 11)

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
        self.assertEqual(move.quantity_done, 5)

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
        self.assertEqual(move.quantity_done, 1)

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
        self.assertEqual(len(first_sales_order.order_line), 4)
        self.assertEqual(first_sales_order.invoice_status, "no")

        downpayment_order_line = first_sales_order.order_line[3]
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
        self.assertEqual(len(first_picking.move_lines), 3)

        first_picking.move_lines[0].quantity_done = 1
        first_picking.move_lines[1].quantity_done = 1  # 2
        first_picking.move_lines[2].quantity_done = 1

        result = first_picking.button_validate()
        self.assertTrue(result)

        wizard = Form(
            self.env[(result.get("res_model"))].with_context(result["context"])
        ).save()
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
        self.assertEqual(len(second_picking.move_lines), 3)

        second_picking.move_lines[0].quantity_done = 3
        second_picking.move_lines[1].quantity_done = 3  # 11
        second_picking.move_lines[2].quantity_done = 3  # 5

        result = second_picking.button_validate()
        self.assertTrue(result)

        wizard = Form(
            self.env[(result.get("res_model"))].with_context(result["context"])
        ).save()
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

        # TODO: questo test fallisce perche non viene per qualche motivo settato il
        #  first_delivery_note in una delle fatture... da capire il perchè.

        first_sales_order._create_invoices()
        self.assertEqual(len(first_sales_order.order_line), 4)
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
        #
        # TODO: self.assertEqual(first_delivery_note.state, 'invoiced')?
        #
        self.assertEqual(len(first_delivery_note.invoice_ids), 2)
        self.assertEqual(first_delivery_note.invoice_ids[0], first_partial_invoice)
        self.assertEqual(first_delivery_note.invoice_ids[1], second_partial_invoice)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        first_backorder = StockPicking.search([("backorder_id", "=", first_picking.id)])
        self.assertEqual(len(first_backorder), 1)
        self.assertEqual(len(first_backorder.move_lines), 1)

        first_backorder.move_lines[0].quantity_done = 1

        result = first_backorder.button_validate()
        self.assertTrue(result)

        #
        # =      =  -  =    = - =    =  -  =      =
        #

        second_backorder = StockPicking.search(
            [("backorder_id", "=", second_picking.id)]
        )
        self.assertEqual(len(second_backorder), 1)
        self.assertEqual(len(second_backorder.move_lines), 2)

        second_backorder.move_lines[0].quantity_done = 8
        second_backorder.move_lines[1].quantity_done = 2

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
        self.assertEqual(move.quantity_done, 1)

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
        self.assertEqual(moves[0].quantity_done, 1)

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
        self.assertEqual(move.quantity_done, 1)

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
        self.assertEqual(move.quantity_done, 3)

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
        self.assertEqual(moves[0].quantity_done, 3)

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
        self.assertEqual(moves[0].quantity_done, 3)

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

        self.assertEqual(len(first_sales_order.order_line), 4)
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
        self.assertEqual(moves[1].quantity_done, 1)

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
        order_line = first_sales_order.order_line[3]
        self.assertEqual(order_line.invoice_status, "invoiced")
        self.assertEqual(order_line.qty_to_invoice, 0)
        self.assertEqual(order_line.qty_invoiced, 0)

        move = order_line.move_ids
        self.assertEqual(len(move), 0)

        delivery_notes = first_delivery_note | second_delivery_note
        delivery_note_line = delivery_notes.mapped("line_ids").filtered(
            lambda l: l.sale_line_id == order_line
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
        self.assertEqual(moves[1].quantity_done, 8)

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
        self.assertEqual(moves[1].quantity_done, 2)

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
        picking.move_lines[0].quantity_done = 1
        picking.button_validate()
        sales_order._create_invoices()
        wizard = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                active_ids=picking.ids, active_model="stock.picking"
            )
        ).save()
        result = wizard.confirm()
        delivery_note = self.env["stock.delivery.note"].browse(result["res_id"])
        delivery_note.action_confirm()
        delivery_note.action_cancel()
        delivery_note.action_draft()
        self.assertEqual(delivery_note.invoice_status, "no")
        self.assertEqual(delivery_note.state, "draft")

    def test_invoicing_multiple_dn(self):
        user = new_test_user(
            self.env,
            login="test_multiple_dn",
            groups="stock.group_stock_manager,"
            "l10n_it_delivery_note.use_advanced_delivery_notes",
        )
        self.env.user = user
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
        self.assertEqual(len(picking.move_lines), 2)

        # deliver only half of the first product
        picking.move_lines[0].quantity_done = 1
        res_dict = picking.button_validate()
        wizard = Form(
            self.env[(res_dict.get("res_model"))]
            .with_user(user)
            .with_context(res_dict["context"])
        ).save()
        wizard.process()
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))]
            .with_user(user)
            .with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        self.assertTrue(picking.delivery_note_id)
        dn = picking.delivery_note_id
        self.assertEqual(dn.partner_id, self.recipient)
        dn.action_confirm()
        dn.action_done()
        picking_backorder = StockPicking.search([("backorder_id", "=", picking.id)])
        self.assertEqual(len(picking_backorder.move_lines), 2)
        picking_backorder.move_lines[0].quantity_done = 1
        picking_backorder.move_lines[1].quantity_done = 1
        picking_backorder.button_validate()
        self.assertEqual(picking_backorder.state, "done")
        back_res_dict = picking_backorder.action_delivery_note_create()
        back_wizard = Form(
            self.env[(back_res_dict.get("res_model"))]
            .with_user(user)
            .with_context(back_res_dict["context"])
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
        self.assertEqual(
            sum(
                invoice.invoice_line_ids.filtered(
                    lambda inv_line: inv_line.product_id.id
                    == self.right_corner_desk_line[2]["product_id"]
                ).mapped("quantity")
            ),
            2,
        )
        self.assertEqual(
            invoice.invoice_line_ids.filtered(
                lambda inv_line: inv_line.product_id.id
                == self.desk_combination_line[2]["product_id"]
            ).quantity,
            1,
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
        invoice_lines = invoice.invoice_line_ids.sorted("sequence")
        for delivery_note in invoice_lines.mapped("delivery_note_id"):
            inv_dn_lines = invoice_lines.filtered(
                lambda l, dn=delivery_note: l.delivery_note_id == dn
            )
            note_line = inv_dn_lines.filtered(lambda l: l.note_dn)
            self.assertEqual(len(note_line), 1)
            # Check that the first line of a particular dn is a note
            self.assertEqual(inv_dn_lines[0], note_line)
            # Check that all lines of a particular dn are neighbouring each other
            self.assertEqual(
                len(inv_dn_lines),
                int(inv_dn_lines[-1].sequence) - int(inv_dn_lines[0].sequence) + 1,
            )

    def test_invoicing_multi_dn_multi_so_same_product(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "l10n_it_delivery_note.group_use_advanced_delivery_notes", True
        )
        # SO 1
        so_1 = self.create_sales_order([self.right_corner_desk_line])  # qty 2
        so_1.action_confirm()

        picking = so_1.picking_ids
        picking.move_lines[0].quantity_done = 1
        res_dict = picking.button_validate()
        # create backorder
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()
        # create delivery note
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
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
        backorder_so_1.move_lines[0].quantity_done = 1
        backorder_so_1.button_validate()
        res_dict = backorder_so_1.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
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
        picking.move_lines[0].quantity_done = 2
        picking.button_validate()
        res_dict = picking.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
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

    def test_invoicing_multi_partial_dn_multi_so_same_product(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "l10n_it_delivery_note.group_use_advanced_delivery_notes", True
        )
        # SO 1
        so_1 = self.create_sales_order([self.right_corner_desk_line])  # qty 2
        so_1.action_confirm()

        # create picking 1.1
        picking_1_1 = so_1.picking_ids
        picking_1_1.move_lines[0].quantity_done = 1
        res_dict = picking_1_1.button_validate()

        # create picking 1.2
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()

        # create delivery note 1.1
        res_dict = picking_1_1.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1_1 = picking_1_1.delivery_note_id
        self.assertTrue(dn_1_1)
        self.assertEqual(dn_1_1.partner_id, self.recipient)
        dn_1_1.action_confirm()
        dn_1_1.action_done()

        # deliver picking 1.2 (but not confirm)
        picking_1_2 = picking_1_1.backorder_ids
        picking_1_2.move_lines[0].quantity_done = 1
        picking_1_2.button_validate()
        res_dict = picking_1_2.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_common = picking_1_2.delivery_note_id

        # SO 2
        so_2 = self.create_sales_order([self.right_corner_desk_line])  # qty 2
        so_2.action_confirm()

        # picking 2.1
        picking_2_1 = so_2.picking_ids
        picking_2_1.move_lines[0].quantity_done = 1
        res_dict = picking_2_1.button_validate()

        # picking 2.2
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()
        picking_2_2 = picking_2_1.backorder_ids

        # create delivery note 2.1
        res_dict = picking_2_1.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_2_1 = picking_2_1.delivery_note_id
        dn_2_1.action_confirm()
        dn_2_1.action_done()

        # deliver 2.2
        picking_2_2.move_lines[0].quantity_done = 1
        picking_2_2.button_validate()
        picking_2_2.delivery_note_id = dn_common
        dn_common.action_confirm()
        dn_common.action_done()
        self.assertEqual(picking_1_2.delivery_note_id, picking_2_2.delivery_note_id)

        # invoice backorder of so_1 and so_2 together
        (so_1 | so_2)._create_invoices()
        self.assertEqual(so_1.invoice_ids, so_2.invoice_ids)
        invoice_lines = so_1.invoice_ids.invoice_line_ids.sorted("sequence")
        dn_inv_lines = invoice_lines.filtered(lambda l: l.note_dn)
        product_inv_lines = invoice_lines - dn_inv_lines
        self.assertEqual(len(dn_inv_lines), 3)
        self.assertEqual(len(product_inv_lines), 4)
        self.assertTrue(all(ln == 1 for ln in product_inv_lines.mapped("quantity")))

    def test_invoicing_multi_partial_dn_multi_so_same_product_not_invoiced(self):
        # Create a sale order with 2 rows with the same product and deliver partly first
        # row and invoice it, than deliver partly again the first row two times and
        # deliver partly the second row, all in different delivery notes. Then invoice
        # all but the second delivery note of the first line.
        self.env["ir.config_parameter"].sudo().set_param(
            "l10n_it_delivery_note.group_use_advanced_delivery_notes", "True"
        )
        # SO 1
        so_1 = self.create_sales_order(
            [
                self.prepare_sales_order_line(
                    self.env.ref("product.product_product_5"), 10
                ),
                self.prepare_sales_order_line(
                    self.env.ref("product.product_product_5"), 10
                ),
            ]
        )
        so_1.action_confirm()

        # create picking 1.1
        picking_1_1 = so_1.picking_ids
        self.assertEqual(len(so_1.picking_ids), 1)
        picking_1_1.move_lines[0].quantity_done = 2
        res_dict = picking_1_1.button_validate()

        # create picking 1.2
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()

        # create delivery note 1.1
        res_dict = picking_1_1.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1_1 = picking_1_1.delivery_note_id
        self.assertTrue(dn_1_1)
        self.assertEqual(dn_1_1.partner_id, self.recipient)
        dn_1_1.action_confirm()
        dn_1_1.action_done()

        # invoice delivery note 1.1
        so_1._create_invoices()
        self.assertTrue(len(so_1.invoice_ids), 1)
        invoice_lines = so_1.invoice_ids.invoice_line_ids.sorted("sequence")
        dn_inv_lines = invoice_lines.filtered(lambda l: l.note_dn)
        product_inv_lines = invoice_lines - dn_inv_lines
        self.assertEqual(len(dn_inv_lines), 1)
        self.assertEqual(len(product_inv_lines), 1)
        self.assertTrue(all(ln == 2 for ln in product_inv_lines.mapped("quantity")))

        # create and validate second delivery note, to do not be invoiced
        # validate picking 1.2
        self.assertEqual(len(so_1.picking_ids), 2)
        picking_1_2 = so_1.picking_ids - picking_1_1
        picking_1_2.move_lines[0].quantity_done = 3
        res_dict = picking_1_2.button_validate()

        # create picking 1.3
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()

        # create delivery note 1.2
        res_dict = picking_1_2.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1_2 = picking_1_2.delivery_note_id
        self.assertTrue(dn_1_2)
        self.assertEqual(dn_1_2.partner_id, self.recipient)
        dn_1_2.action_confirm()
        dn_1_2.action_done()

        # create and validate third delivery note
        # validate picking 1.3
        self.assertEqual(len(so_1.picking_ids), 3)
        picking_1_3 = so_1.picking_ids - (picking_1_1 | picking_1_2)
        picking_1_3.move_lines[0].quantity_done = 4
        res_dict = picking_1_3.button_validate()

        # create picking 1.4
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()

        # create delivery note 1.3
        res_dict = picking_1_3.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1_3 = picking_1_3.delivery_note_id
        self.assertTrue(dn_1_3)
        self.assertEqual(dn_1_3.partner_id, self.recipient)
        dn_1_3.action_confirm()
        dn_1_3.action_done()

        # create and validate fourth delivery note
        # validate picking 1.4
        self.assertEqual(len(so_1.picking_ids), 4)
        picking_1_4 = so_1.picking_ids - (picking_1_1 | picking_1_2 | picking_1_3)
        picking_1_4.move_lines[1].quantity_done = 4
        res_dict = picking_1_4.button_validate()

        # create picking 1.5
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.process()

        # create delivery note 1.4
        res_dict = picking_1_4.action_delivery_note_create()
        wizard = Form(
            self.env[(res_dict.get("res_model"))].with_context(res_dict["context"])
        ).save()
        wizard.confirm()
        dn_1_4 = picking_1_4.delivery_note_id
        self.assertTrue(dn_1_4)
        self.assertEqual(dn_1_4.partner_id, self.recipient)
        dn_1_4.action_confirm()
        dn_1_4.action_done()

        dn_to_invoice = dn_1_3 | dn_1_4
        self.assertTrue(all(dti.state == "done" for dti in dn_to_invoice))
        dn_to_invoice.action_invoice()
        self.assertTrue(all(dti.state == "invoiced" for dti in dn_to_invoice))
        self.assertEqual(dn_1_2.state, "done")
