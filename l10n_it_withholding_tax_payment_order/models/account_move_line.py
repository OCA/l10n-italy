# -*- coding: utf-8 -*-
# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        vals = super(AccountMoveLine, self)._prepare_payment_line_vals(
            payment_order)
        vals['amount_currency'] -= self.withholding_tax_amount
        return vals
