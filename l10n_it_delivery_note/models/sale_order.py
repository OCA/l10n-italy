# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrder(models.Model):
    _inherit = "sale.order"

    default_transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
        default=False,
    )
    default_goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance", string="Appearance of goods", default=False
    )
    default_transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason", string="Reason of transport", default=False
    )
    default_transport_method_id = fields.Many2one(
        "stock.picking.transport.method", string="Method of transport", default=False
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

    def _cancel_delivery_note_lines(self):
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
        draft_delivery_note_lines.write(
            {"invoice_status": DOMAIN_INVOICE_STATUSES[0], "sale_line_id": None}
        )

    def _assign_delivery_notes_invoices(self, invoice_ids):
        if not invoice_ids:
            return

        self._cancel_delivery_note_lines()

        all_invoice_lines = invoice_ids.invoice_line_ids
        for sol in self.order_line:
            if not (sol.is_invoiced and sol.delivery_note_line_ids):
                continue
            dn_lines = sol.delivery_note_line_ids.filtered(
                lambda l: l.is_invoiceable
                and l.delivery_note_id.state
                not in (
                    DOMAIN_DELIVERY_NOTE_STATES[0],  # draft
                    DOMAIN_DELIVERY_NOTE_STATES[-1],  # cancel
                )
            )
            if not dn_lines:
                continue
            inv_lines = all_invoice_lines.filtered(
                lambda line, s=sol: s in line.sale_line_ids
            ).with_context(check_move_validity=False)
            inv_line = inv_lines[0]  # safety guard
            inv_line.write(
                {
                    "delivery_note_line_id": dn_lines[0],
                    "delivery_note_id": dn_lines[0].delivery_note_id,
                }
            )
            if len(dn_lines) > 1:
                inv_line.quantity = dn_lines[0].product_qty
                move_id = inv_line.move_id
                remaining_dn_lines = dn_lines[1:]
                product = sol.product_id
                for dn_line in remaining_dn_lines:
                    move_line = dn_line.move_id.move_line_ids.filtered(
                        lambda l, p=product: l.product_id == p
                    )
                    if len(move_line) != 1:
                        raise UserError(
                            _(
                                "No unique matching move line was found for %(sol)s in"
                                " Stock Move %(move)s"
                            )
                            % {
                                "sol": sol.name,
                                "move": dn_line.move_id.name,
                            }
                        )
                    new_data = inv_line.copy_data(
                        {
                            "quantity": move_line.qty_done,
                            "price_unit": inv_line.price_unit,
                            "delivery_note_line_id": dn_line.id,
                            "delivery_note_id": dn_line.delivery_note_id.id,
                            "sale_line_ids": [(6, 0, inv_line.sale_line_ids.ids)],
                        }
                    )[0]
                    move_id.write({"invoice_line_ids": [(0, 0, new_data)]})
                # We are setting `inv_line.quantity` again because
                # `_move_autocomplete_invoice_lines_write()` applies the new changes on
                # a temporary copy of the original invoice that fetches outdated data
                # thus requiring a second write
                inv_line.quantity = dn_lines[0].product_qty
                move_id._onchange_invoice_line_ids()
            dn_lines.write(
                {
                    "invoice_status": DOMAIN_INVOICE_STATUSES[2],
                }
            )
            for dn in dn_lines.mapped("delivery_note_id"):
                dn.invoice_ids += inv_lines.mapped("move_id")
                dn._compute_invoice_status()
        invoice_ids._check_balanced()

    def _generate_delivery_note_lines(self, invoice_ids):
        invoice_ids.update_delivery_note_lines()

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)

        self._assign_delivery_notes_invoices(invoice_ids)
        self._generate_delivery_note_lines(invoice_ids)

        return invoice_ids


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    delivery_note_line_ids = fields.One2many(
        "stock.delivery.note.line", "sale_line_id", readonly=True
    )
    delivery_picking_id = fields.Many2one("stock.picking", readonly=True, copy=False)

    @property
    def has_picking(self):
        return self.move_ids or (self.is_delivery and self.delivery_picking_id)

    @property
    def is_invoiceable(self):
        return (
            self.invoice_status == DOMAIN_INVOICE_STATUSES[1]
            and self.qty_to_invoice != 0
        )

    @property
    def is_invoiced(self):
        return (
            self.invoice_status != DOMAIN_INVOICE_STATUSES[1] and self.qty_invoiced != 0
        )

    @property
    def need_to_be_invoiced(self):
        return self.product_uom_qty != (self.qty_to_invoice + self.qty_invoiced)

    def fix_qty_to_invoice(self, new_qty_to_invoice=0):
        self.ensure_one()

        cache = {
            "invoice_status": self.invoice_status,
            "qty_to_invoice": self.qty_to_invoice,
        }

        self.write(
            {
                "invoice_status": "to invoice" if new_qty_to_invoice else "no",
                "qty_to_invoice": new_qty_to_invoice,
            }
        )

        return cache

    def is_pickings_related(self, picking_ids):
        if self.is_delivery:
            return self.delivery_picking_id in picking_ids

        return bool(self.move_ids & picking_ids.mapped("move_lines"))

    def retrieve_pickings_lines(self, picking_ids):
        return self.filtered(lambda l: l.has_picking).filtered(
            lambda l: l.is_pickings_related(picking_ids)
        )
