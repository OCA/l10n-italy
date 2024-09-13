# Copyright 2023 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_it_account_stamp_is_stamp_duty_applied = fields.Boolean(
        string="Stamp Duty",
        help="Stamp duty is applied to this invoice.",
        readonly=False,
        compute="_compute_l10n_it_account_stamp_is_stamp_duty_applied",
        store=True,
    )
    l10n_it_account_stamp_is_stamp_duty_present = fields.Boolean(
        string="Stamp line is present in invoice",
        compute="_compute_l10n_it_account_stamp_is_stamp_duty_present",
    )
    l10n_it_account_stamp_auto_compute_stamp_duty = fields.Boolean(
        related="company_id.l10n_it_account_stamp_stamp_duty_product_id.l10n_it_account_stamp_auto_compute",
    )
    l10n_it_account_stamp_manually_apply_stamp_duty = fields.Boolean(
        string="Apply stamp duty",
    )

    def is_stamp_duty_applicable(self):
        stamp_product_id = self.company_id.with_context(
            lang=self.partner_id.lang
        ).l10n_it_account_stamp_stamp_duty_product_id
        if not stamp_product_id:
            raise UserError(_("Missing stamp duty product in company settings!"))
        total_tax_base = sum(
            (
                inv_tax.price_subtotal
                for inv_tax in self.line_ids.filtered(
                    lambda line: set(line.tax_ids.ids)
                    & set(
                        stamp_product_id.l10n_it_account_stamp_stamp_duty_apply_tax_ids.ids
                    )
                )
            ),
            0.0,
        )
        return (
            total_tax_base
            >= stamp_product_id.l10n_it_account_stamp_tax_apply_min_total_base
        )

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "line_ids.price_total",
        "currency_id",
        "company_id",
        "invoice_date",
        "move_type",
        "l10n_it_account_stamp_manually_apply_stamp_duty",
        "invoice_line_ids.tax_ids",
    )
    def _compute_l10n_it_account_stamp_is_stamp_duty_applied(self):
        for invoice in self:
            invoice.l10n_it_account_stamp_is_stamp_duty_applied = False
            if invoice.l10n_it_account_stamp_auto_compute_stamp_duty:
                invoice.l10n_it_account_stamp_is_stamp_duty_applied = (
                    invoice.is_stamp_duty_applicable()
                )
            else:
                if invoice.l10n_it_account_stamp_manually_apply_stamp_duty:
                    invoice.l10n_it_account_stamp_is_stamp_duty_applied = True

    def add_stamp_duty_line(self):
        for inv in self:
            if not inv.l10n_it_account_stamp_is_stamp_duty_applied:
                raise UserError(_("Stamp duty is not applicable"))
            stamp_product_id = inv.company_id.with_context(
                lang=inv.partner_id.lang
            ).l10n_it_account_stamp_stamp_duty_product_id
            if not stamp_product_id:
                raise UserError(_("Missing stamp duty product in company settings!"))
            for line in inv.invoice_line_ids:
                if line.product_id and line.product_id.l10n_it_account_stamp_is_stamp:
                    raise UserError(
                        _("Stamp duty line %s already present. Remove it first.")
                        % line.name
                    )
            stamp_account = stamp_product_id.property_account_income_id
            if not stamp_account:
                raise UserError(
                    _("Missing account income configuration for %s")
                    % stamp_product_id.name
                )
            invoice_line_vals = {
                "move_id": inv.id,
                "product_id": stamp_product_id.id,
                "is_stamp_line": True,
                "name": stamp_product_id.description_sale,
                "sequence": 99999,
                "account_id": stamp_account.id,
                "price_unit": stamp_product_id.list_price,
                "quantity": 1,
                "display_type": "product",
                "product_uom_id": stamp_product_id.uom_id.id,
                "tax_ids": [(6, 0, stamp_product_id.taxes_id.ids)],
            }
            inv.write({"invoice_line_ids": [(0, 0, invoice_line_vals)]})

    def is_stamp_duty_line_present(self):
        self.ensure_one()
        for line in self.line_ids:
            if line.is_stamp_line:
                return True
        return False

    @api.depends(
        "invoice_line_ids",
        "invoice_line_ids.product_id",
        "invoice_line_ids.product_id.l10n_it_account_stamp_is_stamp",
    )
    def _compute_l10n_it_account_stamp_is_stamp_duty_present(self):
        for invoice in self:
            invoice.l10n_it_account_stamp_is_stamp_duty_present = (
                invoice.is_stamp_duty_line_present()
            )

    def is_stamp_duty_product_present(self):
        product_stamp = self.invoice_line_ids.filtered(
            lambda line: line.product_id.l10n_it_account_stamp_is_stamp
        )
        if product_stamp:
            return True
        return False

    def _build_stamp_duty_lines(self, product):
        if (
            not product.property_account_income_id
            or not product.property_account_expense_id
        ):
            raise UserError(
                _("Product %s must have income and expense accounts") % product.name
            )

        income_vals = {
            "name": _("Stamp Duty Income"),
            "is_stamp_line": True,
            "partner_id": self.partner_id.id,
            "account_id": product.property_account_income_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date,
            "debit": 0,
            "credit": product.list_price,
            "display_type": "cogs",
            "currency_id": self.currency_id.id,
        }
        if self.move_type == "out_refund":
            income_vals["debit"] = product.list_price
            income_vals["credit"] = 0

        expense_vals = {
            "name": _("Stamp Duty Expense"),
            "is_stamp_line": True,
            "partner_id": self.partner_id.id,
            "account_id": product.property_account_expense_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date,
            "debit": product.list_price,
            "credit": 0,
            "display_type": "cogs",
            "currency_id": self.currency_id.id,
        }
        if self.move_type == "out_refund":
            income_vals["debit"] = 0
            income_vals["credit"] = product.list_price

        return income_vals, expense_vals

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        for inv in self:
            posted = False
            if (
                inv.l10n_it_account_stamp_is_stamp_duty_applied
                and not inv.is_stamp_duty_line_present()
                and not inv.is_stamp_duty_product_present()
            ):
                if inv.state == "posted":
                    posted = True
                    inv.state = "draft"
                line_model = self.env["account.move.line"]
                stamp_product_id = inv.company_id.with_context(
                    lang=inv.partner_id.lang
                ).l10n_it_account_stamp_stamp_duty_product_id
                if not stamp_product_id:
                    raise UserError(_("Missing stamp duty product in company settings!"))
                income_vals, expense_vals = inv._build_stamp_duty_lines(stamp_product_id)
                income_vals["move_id"] = inv.id
                expense_vals["move_id"] = inv.id
                line_model.with_context(check_move_validity=False).create(income_vals)
                line_model.with_context(check_move_validity=False).create(expense_vals)
                if posted:
                    inv.state = "posted"
        return res

    def button_draft(self):
        res = super().button_draft()
        for account_move in self:
            move_line_stamp_duty_ids = account_move.line_ids.filtered(
                lambda line: line.is_stamp_line
            )
            move_line_stamp_duty_ids.unlink()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    is_stamp_line = fields.Boolean(
        readonly=True
    )  # used only with automatic stamp duty active
