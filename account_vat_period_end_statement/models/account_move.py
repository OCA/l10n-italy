from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def write(self, vals):
        for move in self:
            if "date" in vals and move.date != vals["date"]:
                move.line_ids._check_tax_statement()
        return super().write(vals)
