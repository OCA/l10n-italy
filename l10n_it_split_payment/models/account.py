# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    split_payment = fields.Boolean("Split Payment")


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_sp = fields.Float(
        string="Split Payment",
        digits="Account",
        store=True,
        readonly=True,
        compute="_compute_amount",
    )
    split_payment = fields.Boolean(
        "Is Split Payment", related="fiscal_position_id.split_payment"
    )

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "currency_id",
        "company_id",
        "invoice_date",
        "move_type",
    )
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()
        for move in self:
            move.amount_sp = 0
            if move.fiscal_position_id.split_payment:
                move.amount_sp = move.amount_tax
                move.amount_tax = 0
            move.amount_total = move.amount_untaxed + move.amount_tax

    def _build_debit_line(self):
        if not self.company_id.sp_account_id:
            raise UserError(
                _(
                    "Please set 'Split Payment Write-off Account' field in"
                    " accounting configuration"
                )
            )
        vals = {
            "name": _("Split Payment Write Off"),
            "partner_id": self.partner_id.id,
            "account_id": self.company_id.sp_account_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date or self.invoice_date_due,
            "date_maturity": self.invoice_date or self.invoice_date_due,
            "price_unit": -self.amount_sp,
            "exclude_from_invoice_tab": True,
        }
        return vals

    def _compute_split_payments(self):
        write_off_line_vals = self._build_debit_line()
        write_off_line_vals["move_id"] = self.id
        check = False
        for line in self.line_ids:
            if line.name == _("Split Payment Write Off"):
                check = True
                break
        if not check:
            self.invoice_line_ids.create(write_off_line_vals)

    def action_post(self):
        for move in self:
            if move.split_payment:
                if move.move_type in ["in_invoice", "in_refund"]:
                    raise UserError(
                        _("Can't handle supplier invoices with split payment")
                    )
                move._compute_split_payments()
        res = super(AccountMove, self).action_post()
        return res
