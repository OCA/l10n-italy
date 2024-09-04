from odoo import models


class MoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_payment_line_vals(self, payment_order):
        vals = super()._prepare_payment_line_vals(payment_order)
        if self.withholding_tax_amount:
            vals["amount_currency"] -= self.withholding_tax_amount
        return vals
