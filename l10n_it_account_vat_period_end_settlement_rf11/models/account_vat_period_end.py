# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import UserError


class AccountVatPeriodEndStatement(models.Model):
    _inherit = "account.vat.period.end.statement"

    tax_74_ter_move_id = fields.Many2one(
        comodel_name="account.move",
        string="74ter Tax Entry",
        help="Move of 74ter tax",
    )

    net_tax_74_ter = fields.Float(
        string="Net Tax 74ter",
        help="Net tax 74ter",
    )

    tax_74_ter_amount = fields.Float(
        string="74ter Tax Amount",
        help="Amount of 74ter tax",
    )

    tax_74_ter_amount_previous = fields.Float(
        string="74ter Tax Amount of Previous Period",
        help="Amount of 74ter tax of previous period",
    )

    tax_74_ter_amount_total = fields.Float(
        string="74ter Tax Amount Total",
        help="Amount of 74ter tax total",
    )

    def compute_amounts(self):
        res = super().compute_amounts()
        for statement in self:
            taxes_74ter = self.env["account.tax"].search([("is_tax_74ter", "=", True)])
            if not taxes_74ter:
                continue

            tax_74ter_perc = taxes_74ter[0].tax_74ter_amount
            tax_74ter_total = 0.0
            for tax in taxes_74ter:
                for period in statement.date_range_ids:
                    # NB (v18 port): v16 summed account.tax._compute_totals_tax(
                    # ...)[1] (the base balance). In Odoo 18 that helper negates
                    # the base of *purchase* taxes in the "customer" registry
                    # (a reverse-charge fix that did not exist in v16), which
                    # would break the 74-ter "base su base" computation
                    # (sale_base - purchase_base). We therefore read
                    # ``base_balance`` directly, preserving the original signs.
                    tax_74ter_total += tax.with_context(
                        from_date=period.date_start,
                        to_date=period.date_end,
                    ).base_balance

            statement.net_tax_74_ter = tax_74ter_total / (1 + tax_74ter_perc / 100)
            statement.tax_74_ter_amount = tax_74ter_total - statement.net_tax_74_ter

            previous_statements = statement._get_previous_statements()
            if previous_statements and not statement.annual:
                previous_statement = previous_statements[0]
                if previous_statement.tax_74_ter_amount_total < 0:
                    statement.tax_74_ter_amount_previous = (
                        previous_statement.tax_74_ter_amount_total
                    )
                    statement.tax_74_ter_amount_total = (
                        statement.tax_74_ter_amount
                        + statement.tax_74_ter_amount_previous
                    )
                else:
                    statement.tax_74_ter_amount_previous = 0.0
                    statement.tax_74_ter_amount_total = statement.tax_74_ter_amount
            else:
                statement.tax_74_ter_amount_previous = 0.0
                statement.tax_74_ter_amount_total = statement.tax_74_ter_amount

            if statement.tax_74_ter_amount_total > 0:
                for debit_line in statement.debit_vat_account_line_ids:
                    if debit_line.tax_id.is_tax_74ter:
                        debit_line.amount = statement.tax_74_ter_amount_total
                        break

        return res

    def create_move(self):
        res = super().create_move()
        move_obj = self.env["account.move"]
        for statement in self:
            if statement.tax_74_ter_amount_total > 0:
                tax_74_ter = self.env["account.tax"].search(
                    [("is_tax_74ter", "=", True), ("type_tax_use", "=", "sale")]
                )
                tax_74_ter_income_account = tax_74_ter.tax_74_ter_income_account_id
                # v18 port: account.tax.vat_statement_account_id was removed in
                # Odoo 18. The VAT-on-sales account is now sourced from the tax
                # repartition via _get_debit_accounts() -- the same source the
                # settlement itself uses to build its debit VAT lines.
                vat_statement_account = tax_74_ter._get_debit_accounts()
                if len(vat_statement_account) != 1:
                    raise UserError(
                        self.env._(
                            "The 74ter sale tax '%s' must have exactly one VAT "
                            "account defined in its repartition lines."
                        )
                        % tax_74_ter.name
                    )
                statement_date = fields.Date.to_string(statement.date)
                move_data = {
                    "ref": self.env._("74 Ter VAT statement") + " - " + statement_date,
                    "date": statement_date,
                    "journal_id": statement.journal_id.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": self.env._("74 Ter VAT statement"),
                                "account_id": tax_74_ter_income_account.id,
                                "debit": statement.tax_74_ter_amount_total,
                                "credit": 0.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": self.env._("74 Ter VAT statement"),
                                "account_id": vat_statement_account.id,
                                "debit": 0.0,
                                "credit": statement.tax_74_ter_amount_total,
                            },
                        ),
                    ],
                }
                move = move_obj.create(move_data)
                statement.write({"tax_74_ter_move_id": move.id})
                move.action_post()
        return res

    def statement_draft(self):
        res = super().statement_draft()
        for statement in self:
            if statement.tax_74_ter_move_id:
                statement.tax_74_ter_move_id.button_cancel()
                statement.tax_74_ter_move_id.with_context(force_delete=True).unlink()
        return res
