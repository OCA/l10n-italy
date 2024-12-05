# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    no_commission = fields.Boolean(string="Without commissions")
    l10n_it_riba_commission_use_due_date = fields.Boolean(
        string="Use RiBa due date for commission",
        help="When commission is set for invoice status 'Payment Date Based', "
        "use the corresponding RiBa's due date instead of the payment date.",
        default=True,
    )

    def _get_reconciled_invoices_partials(self):
        """
        If a partial payment is an sbf Riba payment and the safety days haven't
        passed yet, I exclude the payment from the partials list where commissions
        will be generated.
        """
        (
            invoice_partials,
            exchange_diff_moves,
        ) = super()._get_reconciled_invoices_partials()
        to_remove = []
        for (
            partial,
            amount,
            counterpart_line,
        ) in invoice_partials:
            riba_mv_line = self.env["riba.slip.move.line"].search(
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
        return [
            item for item in invoice_partials if item not in to_remove
        ], exchange_diff_moves


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

    def _get_commission_settlement_date(self):
        commission_settlement_date = super()._get_commission_settlement_date()
        if (
            self.commission_id.invoice_state == "paid_date"
            and self.invoice_id.l10n_it_riba_commission_use_due_date
        ):
            # Assume that the invoice will be paid when all the RiBas are due
            riba_lines = self.object_id.move_id.line_ids.slip_line_ids
            commission_settlement_date = max(
                riba_lines.riba_line_id.mapped("due_date"),
                default=date.min,
            )
        return commission_settlement_date
