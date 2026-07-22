# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, _, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


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
        string="Is Split Payment", related="fiscal_position_id.split_payment"
    )

    def _compute_amount(self):
        res = super()._compute_amount()
        for move in self:
            if move.split_payment:
                if move.tax_totals:
                    move.amount_sp = (
                        move.tax_totals["amount_total"]
                        - move.tax_totals["amount_untaxed"]
                    )
                    move.amount_residual -= move.amount_tax
                    move.amount_tax = 0.0
                else:
                    move.amount_sp = 0.0
                move.amount_total = move.amount_untaxed
            else:
                move.amount_sp = 0.0
        return res

    def write(self, vals):
        sp_moves = self.filtered(lambda am: am.split_payment)
        if sp_moves:
            # Add context key to skip move validity only for split
            # payment moves, otherwise adding for all unconditionally
            # allow to create unbalanced account.move
            super(AccountMove, sp_moves.with_context(check_move_validity=False)).write(
                vals
            )
            # Because Environment context not allow manipulation, and
            # with_context merge old context with new key(s) pass a
            # dictionary without wanted key(s) not working; so need to
            # pass the key we want update with new value
            self_ctx = self.with_context(check_move_validity=True)
            res = super(AccountMove, self_ctx - sp_moves).write(vals)
        else:
            res = super().write(vals)
        if self.env.context.get("skip_split_payment_computation"):
            return res
        self.compute_split_payment()
        container = {"records": self}
        with self._check_balanced(container):
            if "fiscal_position_id" in vals:
                self._compute_amount()
            self.with_context(
                skip_split_payment_computation=True, check_move_validity=False
            ).compute_split_payment()
        return res

    def copy(self, default=None):
        if self.split_payment:
            res = super(AccountMove, self.with_context(check_move_validity=False)).copy(
                default=default
            )
            res.compute_split_payment()
        else:
            res = super().copy(default=default)
        return res

    def _build_writeoff_line(self):
        self.ensure_one()

        if not self.company_id.sp_account_id:
            raise UserError(
                _(
                    "Please set 'Split Payment Write-off Account' field in"
                    " accounting configuration"
                )
            )
        debit = 0
        credit = 0
        move_tax_lines = self.line_ids.filtered(
            lambda line: ((line.display_type == "tax") and (not line.is_split_payment))
        )
        for tax_line in move_tax_lines:
            debit += tax_line.credit
            credit += tax_line.debit
        if debit != 0 and credit != 0:
            if debit >= credit:
                debit = debit - credit
                credit = 0
            else:
                credit = credit - debit
                debit = 0

        vals = {
            "name": _("Split Payment Write Off"),
            "partner_id": self.partner_id.id,
            "account_id": self.company_id.sp_account_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date,
            "date_maturity": self.invoice_date,
            "price_unit": -debit + credit,
            "amount_currency": debit - credit,
            "debit": debit,
            "credit": credit,
            "display_type": "tax",
            "is_split_payment": True,
        }
        return vals

    def compute_split_payment(self):
        for move in self:
            if move.is_sale_document(include_receipts=True):
                line_sp = fields.first(
                    move.line_ids.filtered(lambda move_line: move_line.is_split_payment)
                )
                with move._sync_dynamic_lines(container={"records": move}):
                    if move.split_payment:
                        write_off_line_vals = move._build_writeoff_line()
                        if line_sp:
                            if (
                                float_compare(
                                    line_sp.price_unit,
                                    write_off_line_vals["price_unit"],
                                    precision_rounding=move.currency_id.rounding,
                                )
                                != 0
                            ):
                                line_sp.with_context(
                                    skip_split_payment_computation=True
                                ).write(write_off_line_vals)
                        else:
                            if write_off_line_vals.get("price_unit"):
                                move.with_context(
                                    skip_split_payment_computation=True
                                ).line_ids = [Command.create(write_off_line_vals)]
                    elif line_sp:
                        neutralize_vals = {
                            "debit": 0.0,
                            "credit": 0.0,
                            "amount_currency": 0.0,
                            "price_unit": 0.0,
                            "tax_base_amount": 0.0,
                            "tax_tag_ids": [(6, 0, [])],
                        }
                        move.with_context(
                            skip_split_payment_computation=True,
                            check_move_validity=False,
                        ).write(
                            {"line_ids": [Command.update(line_sp.id, neutralize_vals)]}
                        )
