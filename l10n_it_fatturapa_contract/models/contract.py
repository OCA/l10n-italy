#  Copyright 2024 Roberto Fichera - Level Prime Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    related_documents = fields.One2many(
        comodel_name="fatturapa.related_document_type",
        inverse_name="contract_id",
        string="Related Documents",
        groups="account.group_account_user",
    )

    def _prepare_invoice(self, date_invoice, journal=None):
        invoice_vals, move_form = super(ContractContract, self)._prepare_invoice(
            date_invoice, journal
        )

        if self.related_documents:
            invoice_vals["related_documents"] = [
                (
                    0,
                    0,
                    rec.copy_data(
                        default={"contract_id": False, "contract_line_id": False}
                    )[0],
                )
                for rec in self.related_documents
            ]

        return invoice_vals, move_form
