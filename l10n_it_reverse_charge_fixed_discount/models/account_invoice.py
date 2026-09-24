# Copyright 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def rc_inv_line_vals(self, line):
        """
        Override to copy fixed discount when creating self-invoice lines.

        The account_invoice_fixed_discount module adds a discount_fixed field
        that represents a fixed amount discount. This field needs to be copied
        to the self-invoice lines (similar to how the percentage 'discount'
        field is copied) so that the account_invoice_fixed_discount module
        can apply its logic to compute the correct amounts in the self-invoice.
        """
        vals = super(AccountInvoice, self).rc_inv_line_vals(line)

        # Copy the fixed discount field if it exists and has a value
        # The account_invoice_fixed_discount module will handle the
        # price computation automatically
        if hasattr(line, 'discount_fixed'):
            vals['discount_fixed'] = line.discount_fixed

        return vals
