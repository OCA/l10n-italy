#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import first


class WelfareFundTypeAmount(models.Model):
    _name = "welfare.fund.type.amount"
    _description = "Welfare Fund Type Amount"

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )
    welfare_fund_type_id = fields.Many2one(
        comodel_name="welfare.fund.type",
        required=True,
    )
    amount = fields.Float(
        required=True,
    )
    administration_reference = fields.Char()

    _sql_constraints = [
        (
            "welfare_amount_unique",
            "UNIQUE(welfare_fund_type_id, amount)",
            "Welfare Type and amount must be unique.",
        ),
    ]

    @api.depends(
        "welfare_fund_type_id.name",
        "amount",
    )
    def _compute_name(self):
        for welfare_amount in self:
            name = "[{welfare_code}]: {amount}%".format(
                welfare_code=welfare_amount.welfare_fund_type_id.name,
                amount=welfare_amount.amount,
            )
            welfare_amount.name = name

    def _prepare_grouping_invoice_line(self, invoice_lines):
        """
        Get the values of the Invoice Line
        that represents the Welfare Amount of `invoice_lines`.
        """
        self.ensure_one()
        for invoice_line in invoice_lines:
            if self not in invoice_line.welfare_fund_type_amount_ids:
                raise UserError(
                    _(
                        "Welfare '{welfare}' should be present "
                        "in Invoice Line '{line}'"
                    ).format(
                        welfare=self.display_name,
                        line=invoice_line.display_name,
                    )
                )

        first_line = first(invoice_lines)
        return {
            "name": self.display_name,
            "account_id": first_line.account_id.id,
            "invoice_line_tax_ids": [
                (6, 0, first_line.invoice_line_tax_ids.ids),
            ],
            "invoice_id": first_line.invoice_id.id,
            "welfare_grouping_fund_type_amount_id": self.id,
            "welfare_grouped_invoice_line_ids": [
                (6, 0, invoice_lines.ids),
            ],
            "price_unit": self._get_welfare_amount(invoice_lines),
        }

    def _get_welfare_amount(self, invoice_lines):
        """
        Calculate the Welfare Amount of invoice_lines`.
        """
        self.ensure_one()
        lines_subtotal = sum(invoice_lines.mapped("price_subtotal"))
        return self.amount * lines_subtotal / 100
