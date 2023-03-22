# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import models


class SaleCommissionMakeSettle(models.TransientModel):
    _inherit = "sale.commission.make.settle"

    def _get_agent_lines(self, agent, date_to_agent):
        """
        Exclude outstanding invoices, those with Ri.Ba subject to collection payment
        if at least safety days haven't passed since expiration date and those that
        have manually set the flag 'no_commission' (for example if it has been
        outstanding for years now).
        """
        # removes invoice lines with flag "no_commission" and that have
        # payment term set on Ri.Ba from those get with the original method
        agent_lines = (
            super()
            ._get_agent_lines(agent, date_to_agent)
            .filtered(lambda al: not al.invoice_id.no_commission)
            .filtered(lambda r: r.invoice_payment_term_id.riba)
        )
        for line in agent_lines:
            # removes lines if RiBa is past due or in case it is subject to collection
            # and at least the safety days have not passed since the payment due date,
            # to keep a margin and verify that it has been paid.
            riba_mv_line = self.env["riba.distinta.move.line"].search(
                [("move_line_id.move_id", "=", line.invoice_id.id)]
            )
            riba_type = riba_mv_line.riba_line_id.type
            if line.commission_id.invoice_state == "paid" and (
                line.invoice_id.is_unsolved
                or (
                    (
                        line.invoice_id.invoice_date_due
                        + timedelta(
                            days=riba_mv_line.riba_line_id.config_id.safety_days
                        )
                        > date.today()
                    )
                    and riba_type == "sbf"
                )
            ):
                agent_lines -= line
        return agent_lines
