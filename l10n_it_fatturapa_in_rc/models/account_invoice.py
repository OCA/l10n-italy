#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.tools import float_compare


class InvoiceLine(models.Model):
    _inherit = "account.move.line"

    @api.depends()
    def _compute_rc_flag(self):
        if "fatturapa.attachment.in" in self.env.context.get("active_model", []):
            # this means we are importing an e-invoice,
            # so RC flag is already set, where needed
            for line in self:
                line.rc = line.rc
        else:
            return super()._compute_rc_flag()


class Invoice(models.Model):
    _inherit = "account.move"

    def e_inv_check_amount_tax(self):
        if any(self.invoice_line_ids.mapped("rc")) and self.e_invoice_amount_tax:
            error_message = ""
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_tax = self.amount_tax - amount_added_for_rc
            if (
                float_compare(
                    amount_tax,
                    self.e_invoice_amount_tax,
                    precision_rounding=self.currency_id.rounding,
                )
                != 0
            ):
                error_message = _(
                    "Taxed amount ({bill_amount_tax}) "
                    "does not match with "
                    "e-bill taxed amount ({e_bill_amount_tax})"
                ).format(
                    bill_amount_tax=amount_tax or 0,
                    e_bill_amount_tax=self.e_invoice_amount_tax,
                )
            return error_message
        else:
            return super().e_inv_check_amount_tax()

    def e_inv_check_amount_total(self):
        if any(self.invoice_line_ids.mapped("rc")) and self.e_invoice_amount_total:
            error_message = ""
            amount_added_for_rc = self.get_tax_amount_added_for_rc()
            amount_total = self.amount_total - amount_added_for_rc
            if (
                float_compare(
                    amount_total,
                    self.e_invoice_amount_total,
                    precision_rounding=self.currency_id.rounding,
                )
                != 0
            ):
                error_message = _(
                    "Total amount ({bill_amount_total}) "
                    "does not match with "
                    "e-bill total amount ({e_bill_amount_total})"
                ).format(
                    bill_amount_total=amount_total or 0,
                    e_bill_amount_total=self.e_invoice_amount_total,
                )
            return error_message
        else:
            return super().e_inv_check_amount_total()
