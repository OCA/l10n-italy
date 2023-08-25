# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    no_commission = fields.Boolean(string="Without commissions")


class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"

    def _skip_future_payments(self, date_payment_to):
        if self.invoice_id.is_riba_payment:
            dates = [
                line.date_maturity
                + timedelta(
                    max(
                        line.mapped(
                            "distinta_line_ids.riba_line_id.config_id.safety_days"
                        )
                    )
                )
                for line in self.invoice_id.line_ids.filtered(lambda r: r.date_maturity)
            ]
            if dates:
                return date_payment_to < max(dates)
        return super()._skip_future_payments(date_payment_to)
