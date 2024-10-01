from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_tax_statement(self):
        for line in self.filtered(lambda _l: _l.move_id.posted_before):
            move = line.move_id
            if not move.is_invoice():
                continue
            invoice_account_vat_ids = line.filtered(lambda x: x.tax_line_id).mapped(
                "tax_line_id.vat_statement_account_id"
            )
            if not invoice_account_vat_ids:
                continue
            invoice_date_range_ids = self.env["date.range"].search(
                [
                    ("date_start", "<=", move.date),
                    ("date_end", ">=", move.date),
                ]
            )
            if not invoice_date_range_ids:
                continue
            vat_statement_obj = self.env["account.vat.period.end.statement"]
            vat_statements = vat_statement_obj.search(
                [
                    ("date_range_ids", "in", invoice_date_range_ids.ids),
                    ("state", "!=", "draft"),
                    "|",
                    (
                        "credit_vat_account_line_ids.account_id",
                        "in",
                        invoice_account_vat_ids.ids,
                    ),
                    (
                        "debit_vat_account_line_ids.account_id",
                        "in",
                        invoice_account_vat_ids.ids,
                    ),
                ]
            )
            if vat_statements:
                raise UserError(
                    _(
                        "The operation is refused as it would impact already issued "
                        "tax statements on %s.\n"
                        "Please restore the journal entry date or reset VAT statement "
                        "to draft to proceed."
                    )
                    % (
                        " - ".join(
                            format_date(self.env, x.date) for x in vat_statements
                        )
                    )
                )

    def write(self, vals):
        for line in self:
            if (
                "account_id" in vals
                and line.account_id.id != vals["account_id"]
                or "credit" in vals
                and line.credit != vals["credit"]
                or "debit" in vals
                and line.debit != vals["debit"]
            ):
                line._check_tax_statement()
        return super().write(vals)
