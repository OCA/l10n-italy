# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EInvoiceArticleCode(models.Model):
    _name = "l10n_it_edi.article_code"
    _description = "E-invoice Article Code"

    name = fields.Char(string="Code Type")
    code_val = fields.Char(string="Code Value")
    l10n_it_edi_line_id = fields.Many2one(
        "l10n_it_edi.line", string="Related E-invoice Line", readonly=True
    )
