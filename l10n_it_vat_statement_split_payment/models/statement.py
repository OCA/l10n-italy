# Copyright 2018 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class AccountVatPeriodEndStatement(models.Model):
    _inherit = "account.vat.period.end.statement"

    def compute_amounts(self):

        AccountMoveLine = self.env["account.move.line"]
        StatementGenericAccountLine = self.env["statement.generic.account.line"]

        res = super().compute_amounts()

        if self.env.company and self.env.company.sp_description:
            basename = self.env.company.sp_description

        else:
            basename = _("Write-off tax amount on tax")

        for statement in self:
            statement.generic_vat_account_line_ids = (
                statement.generic_vat_account_line_ids.filtered(
                    lambda x: not x.is_split_payment
                )
            )

            for date_range in statement.date_range_ids:
                acc_move_lines = AccountMoveLine.search(
                    [
                        ("move_id.amount_sp", "!=", 0.0),
                        ("move_id.state", "=", "posted"),
                        ("tax_line_id", "!=", False),
                        ("date", ">=", date_range.date_start),
                        ("date", "<=", date_range.date_end),
                    ]
                )

                if not acc_move_lines:
                    continue

                grouped_lines = acc_move_lines.group_by_account_and_tax()
                date_start_str = date_range.date_start
                date_end_str = date_range.date_end

                date_string = _("from {} to {}").format(date_start_str, date_end_str)

                for group_key in grouped_lines:
                    amount = 0.0

                    for line in grouped_lines[group_key]:
                        amount += line.credit - line.debit

                    name = "{} {} - {}".format(
                        basename, group_key[1].description, date_string
                    )

                    account = statement.company_id.sp_account_id or group_key[0]

                    StatementGenericAccountLine.create(
                        {
                            "name": name,
                            "amount": amount,
                            "account_id": account.id,
                            "statement_id": statement.id,
                            "is_split_payment": True,
                        }
                    )

        return res


class StatementGenericAccountLine(models.Model):
    _inherit = "statement.generic.account.line"

    is_split_payment = fields.Boolean()
