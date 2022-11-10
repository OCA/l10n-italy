# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_note_ids = fields.Many2many(
        "stock.delivery.note", compute="_compute_delivery_notes"
    )
    delivery_note_count = fields.Integer(compute="_compute_delivery_notes")

    default_transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
    )
    default_goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance",
        string="Appearance of goods",
    )
    default_transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason",
        string="Reason of transport",
    )
    default_transport_method_id = fields.Many2one(
        "stock.picking.transport.method",
        string="Method of transport",
    )

    @api.onchange("partner_id")
    def onchange_partner_id_shipping_info(self):
        if self.partner_id:
            values = {
                "default_transport_condition_id": (
                    self.partner_id.default_transport_condition_id
                ),
                "default_goods_appearance_id": (
                    self.partner_id.default_goods_appearance_id
                ),
                "default_transport_reason_id": (
                    self.partner_id.default_transport_reason_id
                ),
                "default_transport_method_id": (
                    self.partner_id.default_transport_method_id
                ),
            }

        else:
            values = {
                "default_transport_condition_id": False,
                "default_goods_appearance_id": False,
                "default_transport_reason_id": False,
                "default_transport_method_id": False,
            }

        self.update(values)

    def _compute_delivery_notes(self):
        for order in self:
            delivery_notes = order.order_line.mapped(
                "delivery_note_line_ids.delivery_note_id"
            )

            order.delivery_note_ids = delivery_notes
            order.delivery_note_count = len(delivery_notes)

    def _assign_delivery_notes_invoices(self, invoice_ids):
        order_lines = self.mapped("order_line").filtered(
            lambda l: l.is_invoiced and l.delivery_note_line_ids
        )

        delivery_note_lines = order_lines.mapped("delivery_note_line_ids").filtered(
            lambda l: l.is_invoiceable
        )
        delivery_notes = delivery_note_lines.mapped("delivery_note_id")

        ready_delivery_notes = delivery_notes.filtered(
            lambda n: n.state != DOMAIN_DELIVERY_NOTE_STATES[0]
        )

        draft_delivery_notes = delivery_notes - ready_delivery_notes
        draft_delivery_note_lines = (
            draft_delivery_notes.mapped("line_ids") & delivery_note_lines
        )

        ready_delivery_note_lines = delivery_note_lines - draft_delivery_note_lines

        #
        # TODO: È necessario gestire il caso di fatturazione splittata
        #        di una stessa riga d'ordine associata ad una sola
        #        picking (e di conseguenza, ad un solo DdT)?
        #       Può essere, invece, un caso "borderline"
        #        da lasciar gestire all'operatore?
        #       Personalmente, non lo gestirei e delegherei
        #        all'operatore questa responsabilità...
        #

        draft_delivery_note_lines.write(
            {"invoice_status": DOMAIN_INVOICE_STATUSES[0], "sale_line_id": None}
        )

        ready_delivery_note_lines.write({"invoice_status": DOMAIN_INVOICE_STATUSES[2]})
        ready_delivery_notes.write(
            {"invoice_ids": [(4, invoice_id) for invoice_id in invoice_ids]}
        )

        ready_delivery_notes._compute_invoice_status()

    def _generate_delivery_note_lines(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        invoices.update_delivery_note_lines()

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)

        self._assign_delivery_notes_invoices(invoice_ids.ids)
        self._generate_delivery_note_lines(invoice_ids.ids)

        return invoice_ids

    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped("delivery_note_ids")
        action = self.env.ref(
            "l10n_it_delivery_note.stock_delivery_note_action"
        ).read()[0]
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

        else:
            action = {"type": "ir.actions.act_window_close"}

        return action
