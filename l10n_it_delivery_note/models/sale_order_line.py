# Copyright 2022 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
        return self.filtered(lambda l: l.has_picking).filtered(
            lambda l: l.is_pickings_related(picking_ids)
        )
