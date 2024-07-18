# Copyright (c) 2019, Openindustry.it Sas
# @author: Andrea Piovesana <andrea.m.piovesana@gmail.com>

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_note_ids = fields.Many2many(
        "stock.delivery.note", compute="_compute_delivery_notes"
    )
    delivery_note_count = fields.Integer(compute="_compute_delivery_notes")

    def _compute_delivery_notes(self):
        for order in self:
            delivery_notes = order.order_line.mapped(
                "delivery_note_line_ids.delivery_note_id"
            )

            order.delivery_note_ids = delivery_notes
            order.delivery_note_count = len(delivery_notes)

    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped("delivery_note_ids")

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_delivery_note.stock_delivery_note_action"
        )
        action.update(kwargs)
        if len(delivery_notes) > 1:
            action["domain"] = [("id", "in", delivery_notes.ids)]
        elif len(delivery_notes) == 1:
            action["views"] = [
                (
                    self.env.ref(
                        "l10n_it_delivery_note.stock_delivery_note_form_view"
                    ).id,
                    "form",
                )
            ]
            action["res_id"] = delivery_notes.id
