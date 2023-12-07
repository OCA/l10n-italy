# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_split_payment = fields.Boolean()

    def _build_writeoff_line(self):
        self.ensure_one()

        if not self.move_id.company_id.sp_account_id:
            raise UserError(
                _(
                    "Please set 'Split Payment Write-off Account' field in"
                    " accounting configuration"
                )
            )
        vals = {
            "name": _("Split Payment Write Off"),
            "partner_id": self.move_id.partner_id.id,
            "account_id": self.move_id.company_id.sp_account_id.id,
            "journal_id": self.move_id.journal_id.id,
            "date": self.move_id.invoice_date,
            "date_maturity": self.move_id.invoice_date,
            "price_unit": -self.credit,
            "amount_currency": self.credit,
            "debit": self.credit,
            "credit": self.debit,
            "display_type": "tax",
            "is_split_payment": True,
        }
        if self.move_id.move_type == "out_refund":
            vals["amount_currency"] = -self.debit
            vals["debit"] = self.credit
            vals["credit"] = self.debit
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if (
                line.display_type == "tax"
                and line.move_id.split_payment
                and not line.is_split_payment
                and not any(ml.is_split_payment for ml in line.move_id.line_ids)
            ):
                write_off_line_vals = line._build_writeoff_line()
                line.move_id.line_ids = [(0, 0, write_off_line_vals)]
                line.move_id._sync_dynamic_lines(
                    container={"records": line.move_id, "self": line.move_id}
                )
        return lines

    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if (
                line.move_id.split_payment
                and line.display_type == "tax"
                and not line.is_split_payment
            ):
                write_off_line_vals = line._build_writeoff_line()
                line_sp = fields.first(
                    line.move_id.line_ids.filtered(
                        lambda move_line: move_line.is_split_payment
                    )
                )
                if line_sp:
                    if (
                        float_compare(
                            line_sp.price_unit,
                            write_off_line_vals["price_unit"],
                            precision_rounding=line.move_id.currency_id.rounding,
                        )
                        != 0
                    ):
                        line_sp.write(write_off_line_vals)
                else:
                    if line.move_id.amount_sp:
                        line.move_id.line_ids = [(0, 0, write_off_line_vals)]
                line.move_id._sync_dynamic_lines(
                    container={"records": line.move_id, "self": line.move_id}
                )
        return res
