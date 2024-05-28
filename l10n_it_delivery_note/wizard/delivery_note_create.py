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
            company_id = picking_ids[0].company_id
            return self.env["stock.delivery.note.type"].search(
                [("code", "=", type_code), ("company_id", "=", company_id.id)], limit=1
            )

        else:
            return self.env["stock.delivery.note.type"].search(
                [("code", "=", "outgoing")], limit=1
            )

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
        self.check_compliance(self.selected_picking_ids)
        self.update(
            {
                "partner_shipping_id": self.partner_shipping_id,
                "partner_id": self.selected_picking_ids.mapped(
                    "sale_id.partner_invoice_id"
                )
                if self.selected_picking_ids.mapped("sale_id.partner_invoice_id")
                else self.partner_id,
            }
        )

    def _prepare_delivery_note_vals(self, sale_order_id):
        delivery_method_id = self.selected_picking_ids.mapped("carrier_id")[:1]
        return {
            "company_id": (
                self.selected_picking_ids.mapped("company_id")[:1].id or False
            ),
            "partner_sender_id": self.partner_sender_id.id,
            "partner_id": (
                sale_order_id.partner_invoice_id.id
                if sale_order_id.partner_invoice_id
                else self.partner_id.id
            ),
            "partner_shipping_id": self.partner_shipping_id.id,
            "type_id": self.type_id.id,
            "date": self.date,
            "carrier_id": delivery_method_id.partner_id.id,
            "delivery_method_id": delivery_method_id.id,
            "transport_condition_id": (
                sale_order_id
                and sale_order_id.default_transport_condition_id.id
                or self.partner_id.default_transport_condition_id.id
                or self.type_id.default_transport_condition_id.id
            ),
            "goods_appearance_id": (
                sale_order_id
                and sale_order_id.default_goods_appearance_id.id
                or self.partner_id.default_goods_appearance_id.id
                or self.type_id.default_goods_appearance_id.id
            ),
            "transport_reason_id": (
                sale_order_id
                and sale_order_id.default_transport_reason_id.id
                or self.partner_id.default_transport_reason_id.id
                or self.type_id.default_transport_reason_id.id
            ),
            "transport_method_id": (
                sale_order_id
                and sale_order_id.default_transport_method_id.id
                or self.partner_id.default_transport_method_id.id
                or self.type_id.default_transport_method_id.id
            ),
        }

    def confirm(self):
        self.check_compliance(self.selected_picking_ids)

        sale_order_ids = self.mapped("selected_picking_ids.sale_id")
        sale_order_id = sale_order_ids and sale_order_ids[0] or self.env["sale.order"]

        delivery_note = self.env["stock.delivery.note"].create(
            self._prepare_delivery_note_vals(sale_order_id)
        )

        self.selected_picking_ids.write({"delivery_note_id": delivery_note.id})
        if sale_order_id:
            sale_order_id._assign_delivery_notes_invoices(sale_order_id.invoice_ids)

        if self.user_has_groups("l10n_it_delivery_note.use_advanced_delivery_notes"):
            return delivery_note.goto()
