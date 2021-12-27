# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models


class StockDeliveryNoteSelectWizard(models.TransientModel):
    _name = "stock.delivery.note.select.wizard"
    _inherit = "stock.delivery.note.base.wizard"
    _description = "Delivery Note Selector"

    delivery_note_id = fields.Many2one(
        "stock.delivery.note", string="Delivery Note", required=True
    )

    partner_shipping_id = fields.Many2one(
        "res.partner", related="delivery_note_id.partner_shipping_id"
    )

    date = fields.Date(related="delivery_note_id.date")
    type_id = fields.Many2one(
        "stock.delivery.note.type", related="delivery_note_id.type_id"
    )

    picking_ids = fields.Many2many("stock.picking", compute="_compute_fields")

    @api.depends("selected_picking_ids", "delivery_note_id")
    def _compute_fields(self):
        super()._compute_fields()

        if self.delivery_note_id:
            self.picking_ids += self.delivery_note_id.picking_ids
        else:
            self.picking_ids = self.picking_ids

        if self.selected_picking_ids:
            self.picking_ids += self.selected_picking_ids
        else:
            self.picking_ids = self.picking_ids

    def check_compliance(self, pickings):
        super().check_compliance(pickings)

        self._check_delivery_notes(self.selected_picking_ids)

    def confirm(self):
        self.check_compliance(self.picking_ids)
        self.selected_picking_ids.write({"delivery_note_id": self.delivery_note_id.id})

        sale_order_ids = self.selected_picking_ids.sale_id
        sale_order_id = sale_order_ids and sale_order_ids[0] or self.env["sale.order"]
        if sale_order_id:
            sale_order_id._assign_delivery_notes_invoices(sale_order_id.invoice_ids)

        if self.user_has_groups("l10n_it_delivery_note.use_advanced_delivery_notes"):
            return self.delivery_note_id.goto()
