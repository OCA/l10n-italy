# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _compute_totals_tax(self, data):
        res = super(AccountTax, self)._compute_totals_tax(data)
        if self.is_split_payment:
            # res is (tax_name, base, tax, deductible, undeductible)
            # so, in case of SP, SP VAT must not appear as deductible
            return (res[0], res[1], res[2], 0.0, res[4])
        return res
