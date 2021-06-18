# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


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
        string="Is Split Payment", related="fiscal_position_id.split_payment"
    )

    def _compute_amount(self):
        super()._compute_amount()
        for move in self:
            move.amount_sp = 0
            if move.fiscal_position_id.split_payment:
                move.amount_sp = move.amount_tax
                move.amount_tax = 0
            move.amount_total = move.amount_untaxed + move.amount_tax

            if move.fiscal_position_id.split_payment:
                if move.is_purchase_document():
                    raise UserError(
                        _("Can't handle supplier invoices with split payment")
                    )
                else:
                    move._compute_split_payments()

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
            "date": self.invoice_date,
            "debit": self.amount_sp,
            "credit": 0,
            "exclude_from_invoice_tab": True,
            "is_split_payment": True,
        }
        if self.move_type == "out_refund":
            vals["debit"] = 0
            vals["credit"] = self.amount_sp
        return vals

    def set_receivable_line_ids(self):
        """Recompute all account move lines by _recompute_dynamic_lines()
        and set correct receivable lines
        """
        self._recompute_dynamic_lines()
        line_client_ids = self.line_ids.filtered(
            lambda l: l.account_id.id
            == self.partner_id.property_account_receivable_id.id
        )
        if self.move_type == "out_invoice":
            for line_client in line_client_ids:
                inv_total = self.amount_sp + self.amount_total
                if inv_total:
                    receivable_line_amount = (
                        self.amount_total * line_client.debit
                    ) / inv_total
                else:
                    receivable_line_amount = 0
                line_client.with_context(check_move_validity=False).update(
                    {
                        "price_unit": -receivable_line_amount,
                    }
                )
        elif self.move_type == "out_refund":
            for line_client in line_client_ids:
                inv_total = self.amount_sp + self.amount_total
                if inv_total:
                    receivable_line_amount = (
                        self.amount_total * line_client.credit
                    ) / inv_total
                else:
                    receivable_line_amount = 0
                line_client.with_context(check_move_validity=False).update(
                    {
                        "price_unit": -receivable_line_amount,
                    }
                )

    def _compute_split_payments(self):
        write_off_line_vals = self._build_debit_line()
        line_sp = self.line_ids.filtered(
            lambda l: l.is_split_payment or l.name == _("Split Payment Write Off")
        )
        if line_sp:
            if self.move_type == "out_invoice" and float_compare(
                line_sp[0].debit,
                write_off_line_vals["debit"],
                precision_rounding=self.currency_id.rounding,
            ):
                line_sp[0].with_context(check_move_validity=False).update({"debit": 0})
                self.set_receivable_line_ids()
                line_sp[0].debit = write_off_line_vals["debit"]
            elif self.move_type == "out_refund" and float_compare(
                line_sp[0].credit,
                write_off_line_vals["credit"],
                precision_rounding=self.currency_id.rounding,
            ):
                line_sp[0].with_context(check_move_validity=False).update({"credit": 0})
                self.set_receivable_line_ids()
                line_sp[0].credit = write_off_line_vals["credit"]
        else:
            self.set_receivable_line_ids()
            if self.amount_sp:
                self.line_ids = [(0, 0, write_off_line_vals)]


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_split_payment = fields.Boolean(string="Is Split Payment")
