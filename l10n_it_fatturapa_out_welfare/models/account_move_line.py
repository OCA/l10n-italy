#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    welfare_fund_type_amount_ids = fields.Many2many(
        comodel_name="welfare.fund.type.amount",
        string="Welfare Fund Type Amounts",
        help="Welfare Amounts to be applied on this Invoice Line.",
    )
    welfare_grouping_fund_type_amount_id = fields.Many2one(
        comodel_name="welfare.fund.type.amount",
        string="Grouped Welfare Amount",
        help="Welfare Amount represented by this Invoice Line.",
    )
    welfare_grouping_invoice_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="welfare_group_invoice_line_rel",
        column1="grouping_line",
        column2="grouped_line",
        string="Grouping Welfare Invoice Lines",
        help="Invoice Lines that represent this Line's Welfare Amount.",
    )
    welfare_grouped_invoice_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="welfare_group_invoice_line_rel",
        column1="grouped_line",
        column2="grouping_line",
        string="Grouped Welfare Invoice Lines",
        help="Invoice Lines whose Welfare Amount is represented by this Line.",
    )

    def welfare_group_lines(self):
        """
        Group Invoice Lines in `self` based on their Welfare Amount.
        """
        grouped_lines = dict()
        for line in self:
            welfare_amounts = line.welfare_fund_type_amount_ids
            for welfare_amount in welfare_amounts:
                if welfare_amount not in grouped_lines:
                    grouped_lines[welfare_amount] = line
                else:
                    grouped_lines[welfare_amount] |= line
        return grouped_lines

    def _get_to_be_grouped_welfare_lines(self):
        """
        Get invoice lines of `self` whose Welfare Amount
        has to be represented by another invoice line.
        """
        grouped_lines = self.mapped("welfare_grouped_invoice_line_ids")
        welfare_lines = self.filtered("welfare_fund_type_amount_ids")

        to_be_grouped_lines = welfare_lines - grouped_lines
        return to_be_grouped_lines
