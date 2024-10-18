#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    should_regenerate_welfare_lines = fields.Boolean(
        compute="_compute_should_regenerate_welfare_lines",
        store=True,
    )

    @api.depends(
        "invoice_line_ids.welfare_grouped_invoice_line_ids",
        "invoice_line_ids.welfare_fund_type_amount_ids",
    )
    def _compute_should_regenerate_welfare_lines(self):
        for invoice in self:
            lines = invoice.invoice_line_ids
            # Show the button if some lines have yet to be grouped
            to_be_grouped_lines = lines._get_to_be_grouped_welfare_lines()
            invoice.should_regenerate_welfare_lines = to_be_grouped_lines

    def button_regenerate_welfare_lines(self):
        """
        Delete existing grouping Welfare Lines and create new ones.
        """
        self.ensure_one()
        invoice_lines = self.invoice_line_ids
        # Remove previous grouping lines
        grouping_lines = invoice_lines.filtered("welfare_grouping_fund_type_amount_id")
        grouping_lines.unlink()
        invoice_lines = invoice_lines.exists()

        # Create new grouping lines
        welfare_grouped_lines = invoice_lines.welfare_group_lines()
        grouping_lines_sequence = max(invoice_lines.mapped("sequence")) + 1
        welfare_grouping_lines_values = list()
        for welfare_amount, welfare_lines in welfare_grouped_lines.items():
            welfare_grouping_line_values = (
                welfare_amount._prepare_grouping_invoice_line(welfare_lines)
            )
            welfare_grouping_line_values.update(
                sequence=grouping_lines_sequence,
            )
            welfare_grouping_lines_values.append(welfare_grouping_line_values)

        welfare_grouping_lines = self.env[invoice_lines._name].create(
            welfare_grouping_lines_values,
        )
        return welfare_grouping_lines

    def action_post(self):
        need_welfare_invoices = self.filtered("should_regenerate_welfare_lines")
        if need_welfare_invoices:
            raise UserError(
                _("Please regenerate Welfare Lines for invoices: {invoices}").format(
                    invoices=", ".join(
                        need_welfare_invoices.mapped("display_name"),
                    )
                )
            )
        return super().action_post()
