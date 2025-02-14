# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EInvoiceLineOtherData(models.Model):
    _name = "l10n_it_edi.line_other_data"
    _description = "E-invoice line other data"

    l10n_it_edi_line_id = fields.Many2one(
        "l10n_it_edi.line", string="Related E-bill Line", readonly=True
    )
    name = fields.Char(string="Data Type", readonly=True)
    text_ref = fields.Char(string="Text Reference", readonly=True)
    num_ref = fields.Float(string="Number Reference", readonly=True)
    date_ref = fields.Char(string="Date Reference", readonly=True)
