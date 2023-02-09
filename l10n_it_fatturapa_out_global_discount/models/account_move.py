# Copyright 2023 Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_amount_one(self):
        return

    def _recompute_tax_lines(self, **kwargs):
        res = super()._recompute_tax_lines(**kwargs)
        if self.id:
            line_disc = self.line_ids.filtered(lambda l: l.global_discount_item == True)
            if line_disc:
                line_disc.sudo().write({"exclude_from_invoice_tab": False})
        return res
