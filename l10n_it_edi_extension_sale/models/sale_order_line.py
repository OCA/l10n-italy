# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.fields import Command


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"

    related_document_ids = fields.One2many(
        "account.move.related_document",
        "sale_order_line_id",
        string="Related Documents",
        copy=False,
        groups="account.group_account_user,sales_team.group_sale_salesman",
    )
    l10n_it_edi_admin_ref = fields.Char(string="Admin. ref.", size=20, copy=False)

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        if self.related_document_ids:
            invoice_line_documents = vals.get("related_document_ids", list())
            invoice_line_documents.extend(
                Command.link(line_document_id)
                for line_document_id in self.related_document_ids.ids
            )
            vals.update(
                {
                    "related_document_ids": invoice_line_documents,
                }
            )

        if self.l10n_it_edi_admin_ref:
            vals["l10n_it_edi_admin_ref"] = ", ".join(
                filter(
                    None,
                    [
                        vals.get("l10n_it_edi_admin_ref"),
                        self.l10n_it_edi_admin_ref,
                    ],
                )
            )
        return vals

    def unlink(self):
        related_documents = self.mapped("related_document_ids")
        res = super().unlink()
        related_documents.check_unlink().unlink()
        return res
