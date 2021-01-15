# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    tax_stamp = fields.Boolean(
        "Tax Stamp", readonly=False, compute="_compute_tax_stamp", store=True
    )
    auto_compute_stamp = fields.Boolean(
        related="company_id.tax_stamp_product_id.auto_compute"
    )
    manually_apply_tax_stamp = fields.Boolean("Apply tax stamp")

    def is_tax_stamp_applicable(self):
        stamp_product_id = self.env.company.with_context(
            lang=self.partner_id.lang
        ).tax_stamp_product_id
        if not stamp_product_id:
            raise UserError(_("Missing tax stamp product in company settings!"))
        total_tax_base = sum(
            (
                inv_tax.price_subtotal
                for inv_tax in self.line_ids.filtered(
                    lambda line: set(line.tax_ids.ids)
                    & set(stamp_product_id.stamp_apply_tax_ids.ids)
                )
            ),
            0.0,
        )
        return total_tax_base >= stamp_product_id.stamp_apply_min_total_base

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "line_ids.price_total",
        "currency_id",
        "company_id",
        "invoice_date",
        "move_type",
        "manually_apply_tax_stamp",
        "invoice_line_ids.tax_ids",
    )
    def _compute_tax_stamp(self):
        for invoice in self:
            invoice.tax_stamp = False
            if invoice.auto_compute_stamp:
                invoice.tax_stamp = invoice.is_tax_stamp_applicable()
            else:
                if invoice.manually_apply_tax_stamp:
                    invoice.tax_stamp = True

    def add_tax_stamp_line(self):
        for inv in self:
            if not inv.tax_stamp:
                raise UserError(_("Tax stamp is not applicable"))
            stamp_product_id = self.env.company.with_context(
                lang=inv.partner_id.lang
            ).tax_stamp_product_id
            if not stamp_product_id:
                raise UserError(_("Missing tax stamp product in company settings!"))
            for line in inv.invoice_line_ids:
                if line.product_id and line.product_id.is_stamp:
                    raise UserError(
                        _("Tax stamp line %s already present. Remove it first.")
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
                "name": stamp_product_id.description_sale,
                "sequence": 99999,
                "account_id": stamp_account.id,
                "price_unit": stamp_product_id.list_price,
                "quantity": 1,
                "product_uom_id": stamp_product_id.uom_id.id,
                "tax_ids": [(6, 0, stamp_product_id.taxes_id.ids)],
                "analytic_account_id": None,
            }
            inv.write({"invoice_line_ids": [(0, 0, invoice_line_vals)]})

    def is_tax_stamp_line_present(self):
        for line in self.line_ids:
            if line.is_stamp_line:
                return True
        return False

    def is_tax_stamp_product_present(self):
        product_stamp = self.invoice_line_ids.filtered(
            lambda line: line.product_id.is_stamp
        )
        if product_stamp:
            return True
        return False

    def _build_tax_stamp_lines(self, product):
        if (
            not product.property_account_income_id
            or not product.property_account_expense_id
        ):
            raise UserError(
                _("Product %s must have income and expense accounts") % product.name
            )

        income_vals = {
            "name": _("Tax Stamp Income"),
            "is_stamp_line": True,
            "partner_id": self.partner_id.id,
            "account_id": product.property_account_income_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date,
            "debit": 0,
            "credit": product.list_price,
            "exclude_from_invoice_tab": True,
        }
        if self.move_type == "out_refund":
            income_vals["debit"] = product.list_price
            income_vals["credit"] = 0

        expense_vals = {
            "name": _("Tax Stamp Expense"),
            "is_stamp_line": True,
            "partner_id": self.partner_id.id,
            "account_id": product.property_account_expense_id.id,
            "journal_id": self.journal_id.id,
            "date": self.invoice_date,
            "debit": product.list_price,
            "credit": 0,
            "exclude_from_invoice_tab": True,
        }
        if self.move_type == "out_refund":
            income_vals["debit"] = 0
            income_vals["credit"] = product.list_price

        return income_vals, expense_vals

    def _post(self, soft=True):
        res = super(AccountMove, self)._post(soft=soft)
        for inv in self:
            posted = False
            if (
                inv.tax_stamp
                and not inv.is_tax_stamp_line_present()
                and not inv.is_tax_stamp_product_present()
            ):
                if inv.state == "posted":
                    posted = True
                    inv.state = "draft"
                line_model = self.env["account.move.line"]
                stamp_product_id = self.env.company.with_context(
                    lang=inv.partner_id.lang
                ).tax_stamp_product_id
                if not stamp_product_id:
                    raise UserError(_("Missing tax stamp product in company settings!"))
                income_vals, expense_vals = inv._build_tax_stamp_lines(stamp_product_id)
                income_vals["move_id"] = inv.id
                expense_vals["move_id"] = inv.id
                line_model.with_context(check_move_validity=False).create(income_vals)
                line_model.with_context(check_move_validity=False).create(expense_vals)
                if posted:
                    inv.state = "posted"
        return res

    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        for account_move in self:
            move_line_tax_stamp_ids = account_move.line_ids.filtered(
                lambda line: line.is_stamp_line
            )
            move_line_tax_stamp_ids.unlink()
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    is_stamp_line = fields.Boolean(
        readonly=True
    )  # used only with automatic tax stamp active
