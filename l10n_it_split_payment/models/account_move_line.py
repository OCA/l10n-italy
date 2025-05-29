# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_split_payment = fields.Boolean(compute="_compute_is_split_payment", store=True)

    @api.depends("account_id", "company_id.sp_account_id")
    def _compute_is_split_payment(self):
        for line in self:
            line.is_split_payment = False
            if line.account_id == line.company_id.sp_account_id:
                line.is_split_payment = True

    def _build_writeoff_line(self):
        if len(self.mapped("move_id")) != 1:
            raise UserError(
                _("Cannot create a split payment write-off line for multiple moves.")
            )
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
            "price_unit": -sum(self.mapped("credit")),
            "amount_currency": sum(self.mapped("credit")),
            "debit": sum(self.mapped("credit")),
            "credit": sum(self.mapped("debit")),
            "display_type": "tax",
        }
        if self.move_id.move_type == "out_refund":
            vals["amount_currency"] = -sum(self.mapped("debit"))
            vals["debit"] = sum(self.mapped("credit"))
            vals["credit"] = sum(self.mapped("debit"))
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        move_ids = lines.filtered(
            lambda line: line.display_type == "tax"
            and line.move_id.split_payment
            and line.move_id.is_sale_document(include_receipts=True)
            and not line.is_split_payment
            and not any(ml.is_split_payment for ml in line.move_id.line_ids)
        ).mapped("move_id")
        move_ids.compute_split_payment()
        return lines
