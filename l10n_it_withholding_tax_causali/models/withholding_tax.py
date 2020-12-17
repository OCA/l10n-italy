from odoo import fields, models


class WithholdingTax(models.Model):
    _inherit = "withholding.tax"
    payment_reason_id = fields.Many2one("payment.reason", string="Payment reason")
