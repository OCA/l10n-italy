# -*- coding: utf-8 -*-

from odoo import models


class Tax(models.Model):
    _inherit = 'account.tax'

    def get_base_balance_domain(self, state_list, type_list):
        domain = super(Tax, self).get_base_balance_domain(
            state_list, type_list)
        if self.env.context.get("exclude_from_vat_statement_amount"):
            domain.append(('exclude_from_vat_statement_amount', '=', False))
        return domain
