from odoo import fields, models


class WithholdingTax(models.Model):
    _inherit = "withholding.tax"
    causale_pagamento_id = fields.Many2one(
        "causale.pagamento", string="Causale pagamento"
    )
