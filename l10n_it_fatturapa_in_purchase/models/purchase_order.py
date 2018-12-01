# -*- coding: utf-8 -*-

from odoo import models, fields, api


class POLine(models.Model):
    _inherit = 'purchase.order.line'
    to_invoice = fields.Boolean(
        "To Invoice", compute="_compute_to_invoice", store=True)

    @api.depends(
        "invoice_lines.invoice_id.state", "product_qty", "product_uom",
        "invoice_lines.quantity", "invoice_lines.uom_id"
    )
    def _compute_to_invoice(self):
        for line in self:
            if line.product_qty > line.qty_invoiced:
                line.to_invoice = True
            else:
                line.to_invoice = False

    @api.multi
    def name_get(self):
        res = []
        for line in self:
            name = "%s: %s" % (line.order_id.name, line.name)
            res.append((line.id, name))
        return res
