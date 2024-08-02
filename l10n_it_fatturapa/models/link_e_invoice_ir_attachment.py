#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class LinkEInvoiceIRAttachment(models.AbstractModel):
    _name = "l10n_it_fatturapa.attachment.e_invoice.link"
    _description = "Link attachment in current record"

    @api.model
    def _l10n_it_link_attachments(self, attachment_field="ir_attachment_id"):
        """Link self to the attachment in `attachment_field`.

        This allows access to the attachment for
        anyone who can access `self` (see `ir.attachment.check`).
        """
        for e_invoice in self:
            e_invoice[attachment_field].update(
                {
                    "res_model": e_invoice._name,
                    "res_id": e_invoice.id,
                }
            )

    @api.model_create_multi
    def create(self, vals_list):
        e_invoices = super().create(vals_list)
        e_invoices._l10n_it_link_attachments()
        return e_invoices

    def write(self, vals):
        res = super().write(vals)
        self._l10n_it_link_attachments()
        return res
