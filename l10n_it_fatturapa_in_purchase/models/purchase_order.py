# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Simone Rubino - Agile Business Group

from odoo import fields, models
from odoo.tools import float_compare


class POLine(models.Model):
    _inherit = "purchase.order.line"

    to_invoice = fields.Boolean(compute="_compute_qty_invoiced", store=True)

    def _compute_qty_invoiced(self):
        res = super()._compute_qty_invoiced()
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for line in self:
            if float_compare(line.qty_to_invoice, 0.0, precision_digits=precision) == 1:
                line.to_invoice = True
            else:
                line.to_invoice = False
        return res

    def name_get(self):
        res = []
        for line in self:
            name = f"{line.order_id.name}: {line.name}"
            res.append((line.id, name))
        return res
