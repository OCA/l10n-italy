# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl

import functools

from odoo import models


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    def rc_inv_line_vals(self, line):
        line_vals = super().rc_inv_line_vals(line)
        line_vals["discount2"] = line.discount2
        line_vals["discount3"] = line.discount3
        return line_vals

    def get_discount_for_rc(self, line):
        discount_values = [
            1 - (line.discount or 0.0) / 100.0,
            1 - (line.discount2 or 0.0) / 100.0,
            1 - (line.discount3 or 0.0) / 100.0,
        ]
        res = (1 - functools.reduce((lambda x, y: x * y), discount_values)) * 100
        return res
