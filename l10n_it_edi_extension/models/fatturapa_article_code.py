# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FatturapaArticleCode(models.Model):
    _name = "fatturapa.article.code"
    _description = "E-invoice Article Code"

    name = fields.Char(string="Code Type")
    code_val = fields.Char(string="Code Value")
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", string="Related E-invoice Line", readonly=True
    )
