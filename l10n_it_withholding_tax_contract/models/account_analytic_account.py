# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def _prepare_invoice_line(self, line, invoice_id):
        invoice_line_vals = super(AccountAnalyticAccount, self).\
            _prepare_invoice_line(line, invoice_id)
        fiscal_position_id = self.partner_id.property_account_position_id
        invoice_line_vals.update({
            'invoice_line_tax_wt_ids': [
                (6, 0, fiscal_position_id.withholding_tax_ids.ids)]
        })
        return invoice_line_vals

    def recurring_create_invoice(self, limit=None):
        invoices = super(AccountAnalyticAccount, self).\
            recurring_create_invoice(limit)
        invoices._onchange_invoice_line_wt_ids()

        return invoices
