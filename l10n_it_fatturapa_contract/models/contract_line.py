#  Copyright 2024 Roberto Fichera - Level Prime Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    related_documents = fields.One2many(
        comodel_name="fatturapa.related_document_type",
        inverse_name="contract_line_id",
        string="Related Documents",
        groups="account.group_account_user",
    )
    admin_ref = fields.Char(
        string="Admin. ref.",
        copy=False,
        groups="account.group_account_user",
    )

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        invoice_line_vals = super()._prepare_invoice_line(**optional_values)
        contract_documents = self.related_documents
        if contract_documents:
            invoice_line_documents = invoice_line_vals.get("related_documents", list())
            invoice_line_documents.extend(
                (4, line_document_id) for line_document_id in contract_documents.ids
            )
            invoice_line_vals.update(
                {
                    "related_documents": invoice_line_documents,
                }
            )

        contract_admin_ref = self.admin_ref
        if contract_admin_ref:
            invoice_line_admin_ref = invoice_line_vals.get("admin_ref")
            invoice_line_admin_ref = ", ".join(
                filter(
                    None,
                    [
                        invoice_line_admin_ref,
                        contract_admin_ref,
                    ],
                )
            )
            invoice_line_vals.update(
                {
                    "admin_ref": invoice_line_admin_ref,
                }
            )
        return invoice_line_vals
