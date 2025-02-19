# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class FatturapaActivityProgress(models.Model):
    _name = "fatturapa.activity.progress"
    _description = "E-invoice activity progress"

    fatturapa_activity_progress = fields.Integer(string="Activity Progress")
    invoice_id = fields.Many2one(
        "account.move", string="Related Invoice", ondelete="cascade", index=True
    )
