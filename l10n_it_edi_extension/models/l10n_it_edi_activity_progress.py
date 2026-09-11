# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EInvoiceActivityProgress(models.Model):
    _name = "l10n_it_edi.activity_progress"
    _description = "E-invoice activity progress"

    activity_progress = fields.Integer()
    invoice_id = fields.Many2one(
        "account.move", string="Related Invoice", ondelete="cascade", index=True
    )
