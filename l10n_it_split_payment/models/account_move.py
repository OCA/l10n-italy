# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, fields, models
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
                if move.is_purchase_document():
                    continue
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
        res = super().write(vals)
        if self.env.context.get("skip_split_payment_computation"):
            return res
        for move in self:
            if move.split_payment:
                line_sp = fields.first(
                    move.line_ids.filtered(lambda move_line: move_line.is_split_payment)
                )
                for line in move.line_ids:
                    if line.display_type == "tax" and not line.is_split_payment:
                        write_off_line_vals = line._build_writeoff_line()
                        if line_sp:
                            if (
                                float_compare(
                                    line_sp.price_unit,
                                    write_off_line_vals["price_unit"],
                                    precision_rounding=move.currency_id.rounding,
                                )
                                != 0
                            ):
                                line_sp.write(write_off_line_vals)
                        else:
                            if move.amount_sp:
                                move.with_context(
                                    skip_split_payment_computation=True
                                ).line_ids = [Command.create(write_off_line_vals)]
        return res
