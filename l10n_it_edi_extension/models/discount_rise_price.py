# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class DiscountRisePrice(models.Model):
    _name = "discount.rise.price"
    _description = "E-invoice Discount Supplement Data"

    name = fields.Selection([("SC", "Discount"), ("MG", "Supplement")], string="Type")
    percentage = fields.Float()
    amount = fields.Float(digits="Discount")
    invoice_line_id = fields.Many2one(
        "account.move.line",
        string="Related Invoice from line",
        ondelete="cascade",
        index=True,
    )
    invoice_id = fields.Many2one(
        "account.move", string="Related Invoice", ondelete="cascade", index=True
    )
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", string="Related E-invoice Line", readonly=True
    )
