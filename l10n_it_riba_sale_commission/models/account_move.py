# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    no_commission = fields.Boolean(string="Without commissions")

    def _get_reconciled_invoices_partials(self):
        """
        If a partial payment is an sbf Riba payment and the safety days haven't
        passed yet, I exclude the payment from the partials list where commissions
        will be generated.
        """
        res = super()._get_reconciled_invoices_partials()
        to_remove = []
        for (
            partial,
            amount,
            counterpart_line,
        ) in res:
            riba_mv_line = self.env["riba.distinta.move.line"].search(
                [("move_line_id", "=", partial.debit_move_id.id)]
            )
            if riba_mv_line:
                riba_type = riba_mv_line.riba_line_id.type
                if (
                    riba_mv_line.riba_line_id.due_date
                    + timedelta(days=riba_mv_line.riba_line_id.config_id.safety_days)
                    > date.today()
                ) and riba_type == "sbf":
                    to_remove.append((partial, amount, counterpart_line))
        return [item for item in res if item not in to_remove]


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
                        ),
                        default=0,
                    )
                )
                for line in self.invoice_id.line_ids.filtered(lambda r: r.date_maturity)
            ]
            if dates:
                return date_payment_to < max(dates)
        return super()._skip_future_payments(date_payment_to)
