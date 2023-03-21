from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    # RMAs that were created from a delivery note
    rma_ids = fields.One2many(
        comodel_name="rma",
        inverse_name="delivery_note_id",
        string="RMAs",
        copy=False,
    )

    rma_count = fields.Integer(string="RMA count", compute="_compute_rma_count")

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)], "sent": [("readonly", False)]},
        default=lambda self: self.env.user._get_default_warehouse_id(),
        check_company=True,
    )

    def _compute_rma_count(self):
        for record in self:
            record.rma_count = len(record.rma_ids)

    def _prepare_rma_wizard_line_vals(self, data):
        """So we can extend the wizard easily"""
        return {
            "product_id": data["product"].id,
            "quantity": data["quantity"],
            "delivery_note_line_id": data["delivery_note_line_id"].id,
            "uom_id": data["uom"].id,
            "picking_id": data["picking"] and data["picking"].id,
        }

    def action_create_rma(self):
        self.ensure_one()
        if self.state not in ["confirm", "done", "invoiced"]:
            raise ValidationError(
                _(
                    "You may only create RMAs from a "
                    "confirmed or done delivery order."
                )
            )
        wizard_obj = self.env["stock.delivery.note.rma.wizard"]
        line_vals = [
            (0, 0, self._prepare_rma_wizard_line_vals(data))
            for data in self.get_delivery_rma_data()
        ]
        wizard = wizard_obj.with_context(active_id=self.id).create(
            {"line_ids": line_vals, "location_id": self.warehouse_id.rma_loc_id.id}
        )
        return {
            "name": _("Create RMA"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "stock.delivery.note.rma.wizard",
            "res_id": wizard.id,
            "target": "new",
        }

    def action_view_rma(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("rma.rma_action")
        rma = self.rma_ids
        if len(rma) == 1:
            action.update(
                res_id=rma.id,
                view_mode="form",
                views=[],
            )
        else:
            action["domain"] = [("id", "in", rma.ids)]
        # reset context to show all related rma without default filters
        action["context"] = {}
        return action

    def get_delivery_rma_data(self):
        self.ensure_one()
        data = []
        for line in self.line_ids:
            data += line.prepare_delivery_rma_data()
        return data

    @api.depends("rma_ids.refund_id")
    def _get_invoiced(self):
        """Search for possible RMA refunds and link them to the delivery note. We
        don't want to link their delivery note lines as that would unbalance the
        qtys to invoice wich isn't correct for this case"""
        super()._get_invoiced()
        for delivery_note in self:
            refunds = delivery_note.sudo().rma_ids.mapped("refund_id")
            if not refunds:
                continue
            delivery_note.write(
                {
                    "invoice_ids": delivery_note.invoice_ids + refunds,
                    "invoice_count": len(delivery_note.invoice_ids),
                }
            )


class StockDeliveryNoteLine(models.Model):
    _inherit = "stock.delivery.note.line"

    delivery_move_ids = fields.One2many(
        "stock.move", "delivery_note_line_id", string="Delivery Transfers"
    )

    def prepare_delivery_rma_data(self):
        self.ensure_one()
        # Method helper to filter chained moves

        def destination_moves(_move):
            return _move.mapped("move_dest_ids").filtered(
                lambda r: r.state in ["partially_available", "assigned", "done"]
            )

        if self.product_id.type not in ["product", "consu"]:
            return {}
        moves = self.move_id
        data = []
        if moves:
            for move in moves:
                # Look for chained moves to check how many items we can allow
                # to return. When a product is re-delivered it should be
                # allowed to open an RMA again on it.
                qty = move.product_qty
                qty_returned = 0
                move_dest = destination_moves(move)
                # With the return of the return of the return we could have an
                # infinite loop, so we should avoid it dropping already explored
                # move_dest_ids
                visited_moves = move + move_dest
                while move_dest:
                    qty_returned -= sum(move_dest.mapped("product_qty"))
                    move_dest = destination_moves(move_dest) - visited_moves
                    if move_dest:
                        visited_moves += move_dest
                        qty += sum(move_dest.mapped("product_qty"))
                        move_dest = destination_moves(move_dest) - visited_moves
                # If by chance we get a negative qty we should ignore it
                qty = max(0, sum((qty, qty_returned)))
                data.append(
                    {
                        "product": move.product_id,
                        "quantity": qty,
                        "uom": move.product_uom,
                        "picking": move.picking_id,
                        "delivery_note_line_id": self,
                    }
                )
        else:
            data.append(
                {
                    "product": self.product_id,
                    "quantity": self.product_qty,
                    "uom": self.product_uom_id,
                    "picking": False,
                    "delivery_note_line_id": self,
                }
            )
        return data
