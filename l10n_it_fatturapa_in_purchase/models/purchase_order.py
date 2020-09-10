# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Simone Rubino - Agile Business Group

from odoo import models, fields, api
from odoo.tools import float_compare


class POLine(models.Model):
    _inherit = 'purchase.order.line'
    to_invoice = fields.Boolean(
        "To Invoice", compute="_compute_to_invoice", store=True)

    @api.depends(
        "invoice_lines.invoice_id.state", "product_qty", "product_uom",
        "invoice_lines.quantity", "invoice_lines.uom_id"
    )
    def _compute_to_invoice(self):
        precision = self.env['decimal.precision'] \
            .precision_get('Product Unit of Measure')
        for line in self:
            if line.product_id.purchase_method == 'purchase':
                qty_to_invoice = line.product_qty
            else:
                qty_to_invoice = line.qty_received

            if float_compare(line.qty_invoiced, qty_to_invoice,
                             precision_digits=precision) == -1:
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
