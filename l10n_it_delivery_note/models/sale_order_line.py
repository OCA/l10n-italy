# Copyright 2022 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

from odoo import fields, models

from .stock_delivery_note import DOMAIN_INVOICE_STATUSES


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

        return bool(self.move_ids & picking_ids.mapped("move_ids"))

    def retrieve_pickings_lines(self, picking_ids):
        return self.filtered(lambda line: line.has_picking).filtered(
            lambda line: line.is_pickings_related(picking_ids)
        )

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        invoiced_dn_lines = self.env.context.get(
            "delivery_note_invoiced_lines",
            self.env["stock.delivery.note.line"].browse(),
        )
        invoiceable_dn_lines = (
            self.delivery_note_line_ids.filtered(
                lambda dn_line: dn_line.is_invoiceable
                and self.product_id == dn_line.product_id
            )
            - invoiced_dn_lines
        )
        invoicing_delivery_notes = self.env.context.get(
            "invoicing_delivery_notes",
            self.env["stock.delivery.note"].browse(),
        )
        if invoicing_delivery_notes:
            invoiceable_dn_lines = invoiceable_dn_lines.filtered(
                lambda dn_line: dn_line.delivery_note_id in invoicing_delivery_notes
            )

        if invoiceable_dn_lines:
            invoiced_dn_line = fields.first(invoiceable_dn_lines)
            values.update(
                {
                    "delivery_note_line_id": invoiced_dn_line.id,
                    "quantity": math.copysign(
                        invoiced_dn_line.product_qty,
                        values.get("quantity", 1),
                    ),
                }
            )
            self.env.context = dict(
                self.env.context,
                delivery_note_invoiced_lines=invoiced_dn_lines | invoiced_dn_line,
            )
        return values
