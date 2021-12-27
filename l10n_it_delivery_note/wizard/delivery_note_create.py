# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

import datetime

from odoo import api, fields, models

from ..mixins.picking_checker import PICKING_TYPES


class StockDeliveryNoteCreateWizard(models.TransientModel):
    _name = "stock.delivery.note.create.wizard"
    _inherit = "stock.delivery.note.base.wizard"
    _description = "Delivery Note Creator"

    def _default_date(self):
        return datetime.date.today()

    def _default_type(self):
        active_ids = self.env.context.get("active_ids", [])
        picking_ids = self.env["stock.picking"].browse(active_ids)
        if picking_ids:
            type_code = picking_ids[0].picking_type_id.code

            return self.env["stock.delivery.note.type"].search(
                [("code", "=", type_code)], limit=1
            )

        else:
            return self.env["stock.delivery.note.type"].search(
                [("code", "=", "outgoing")], limit=1
            )

    partner_shipping_id = fields.Many2one("res.partner", required=True)

    date = fields.Date(default=_default_date)
    type_id = fields.Many2one(
        "stock.delivery.note.type", default=_default_type, required=True
    )
    picking_type = fields.Selection(
        PICKING_TYPES, string="Picking type", compute="_compute_picking_type"
    )

    @api.depends("selected_picking_ids")
    def _compute_picking_type(self):
        picking_types = set(self.selected_picking_ids.mapped("picking_type_code"))
        picking_types = list(picking_types)

        if len(picking_types) != 1:
            raise ValueError(
                "You have just called this method on an "
                "heterogeneous set of pickings.\n"
                "All pickings should have the same "
                "'picking_type_code' field value."
            )

        self.picking_type = picking_types[0]

    @api.model
    def check_compliance(self, pickings):
        super().check_compliance(pickings)

        self._check_delivery_notes(pickings)

    @api.onchange("partner_id")
    def _onchange_partner(self):
        self.partner_shipping_id = self.partner_id

    def confirm(self):
        self.check_compliance(self.selected_picking_ids)

        sale_order_ids = self.mapped("selected_picking_ids.sale_id")
        sale_order_id = sale_order_ids and sale_order_ids[0] or self.env["sale.order"]

        delivery_note = self.env["stock.delivery.note"].create(
            {
                "partner_sender_id": self.partner_sender_id.id,
                "partner_id": self.partner_id.id,
                "partner_shipping_id": self.partner_shipping_id.id,
                "type_id": self.type_id.id,
                "date": self.date,
                "delivery_method_id": self.partner_id.property_delivery_carrier_id.id,
                "transport_condition_id": sale_order_id
                and sale_order_id.default_transport_condition_id.id
                or self.partner_id.default_transport_condition_id.id
                or self.type_id.default_transport_condition_id.id,
                "goods_appearance_id": sale_order_id
                and sale_order_id.default_goods_appearance_id.id
                or self.partner_id.default_goods_appearance_id.id
                or self.type_id.default_goods_appearance_id.id,
                "transport_reason_id": sale_order_id
                and sale_order_id.default_transport_reason_id.id
                or self.partner_id.default_transport_reason_id.id
                or self.type_id.default_transport_reason_id.id,
                "transport_method_id": sale_order_id
                and sale_order_id.default_transport_method_id.id
                or self.partner_id.default_transport_method_id.id
                or self.type_id.default_transport_method_id.id,
            }
        )

        self.selected_picking_ids.write({"delivery_note_id": delivery_note.id})
        if sale_order_id:
            sale_order_id._assign_delivery_notes_invoices(sale_order_id.invoice_ids)

        if self.user_has_groups("l10n_it_delivery_note.use_advanced_delivery_notes"):
            return delivery_note.goto()
