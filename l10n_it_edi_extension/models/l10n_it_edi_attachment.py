# Copyright 2026 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class L10nItEdiAttachment(models.Model):
    _name = "l10n_it_edi.attachment"
    _description = "E-invoice attachment"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    compression = fields.Char(size=10)
    format = fields.Char(size=10)
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        attachments = super().create(vals_list)
        attachments._l10n_it_edi_link_invoice()
        return attachments

    def write(self, vals):
        res = super().write(vals)
        if "invoice_id" in vals:
            self._l10n_it_edi_link_invoice()
        return res

    def _l10n_it_edi_link_invoice(self):
        """Link the underlying attachment to the invoice.

        This allows access to the attachment for
        anyone who can access the invoice (see ``ir.attachment.check``).
        """
        for attachment in self:
            if not attachment.invoice_id:
                continue
            ir_attachment = attachment.ir_attachment_id
            if (ir_attachment.res_model, ir_attachment.res_id) != (
                "account.move",
                attachment.invoice_id.id,
            ):
                ir_attachment.sudo().write(
                    {
                        "res_model": "account.move",
                        "res_id": attachment.invoice_id.id,
                    }
                )
