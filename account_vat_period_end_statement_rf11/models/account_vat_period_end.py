# Copyright 2024 Innovyou srl <http://www.innovyou.it>

from odoo import models, fields, _

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
            taxes_74ter = self.env['account.tax'].search([('is_tax_74ter', '=', True)])

            tax_74ter_perc = taxes_74ter[0].tax_74ter_amount
            tax_74ter_total = 0.0
            tax_74ter_data = []
            for tax in taxes_74ter:
                for date_range in statement.date_range_ids:
                    tax_74ter_data = tax._compute_totals_tax(
                        {
                            "from_date": date_range.date_start,
                            "to_date": date_range.date_end,
                        }
                    )
                    tax_74ter_total += tax_74ter_data[1]

            statement.net_tax_74_ter = tax_74ter_total / (1 + tax_74ter_perc / 100)
            statement.tax_74_ter_amount = tax_74ter_total - statement.net_tax_74_ter

            previous_statements = statement._get_previous_statements()
            if previous_statements and not statement.annual:
                previous_statement = previous_statements[0]
                if previous_statement.tax_74_ter_amount_total < 0:
                    statement.tax_74_ter_amount_previous = previous_statement.tax_74_ter_amount_total
                    statement.tax_74_ter_amount_total = statement.tax_74_ter_amount + statement.tax_74_ter_amount_previous
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
                tax_74_ter = self.env["account.tax"].search([("is_tax_74ter", "=", True), ("type_tax_use", "=", "sale")])
                tax_74_ter_income_account = tax_74_ter.tax_74_ter_income_account_id
                vat_statement_account = tax_74_ter.vat_statement_account_id
                statement_date = fields.Date.to_string(statement.date)
                move_data = {
                    "name": _("74 Ter VAT statement") + " - " + statement_date,
                    "date": statement_date,
                    "journal_id": statement.journal_id.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": _("74 Ter VAT statement"),
                                "account_id": tax_74_ter_income_account.id,
                                "debit": statement.tax_74_ter_amount_total,
                                "credit": 0.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": _("74 Ter VAT statement"),
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