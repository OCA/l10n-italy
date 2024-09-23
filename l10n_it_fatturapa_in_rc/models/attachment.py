#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class Attachment(models.Model):
    _inherit = "fatturapa.attachment.in"

    @api.model_create_multi
    def create(self, vals_list):
        attachments = super().create(vals_list)
        rc_invoices = self.env["account.move"].search(
            [
                ("move_type", "in", ("in_invoice", "in_refund")),
                ("rc_self_invoice_id", "!=", False),
                ("fatturapa_attachment_in_id", "=", False),
            ],
        )
        for attachment in attachments:
            if attachment.linked_invoice_id_xml and attachment.is_self_invoice:
                rc_invoice = rc_invoices.filtered(
                    lambda i, att=attachment: i.name == att.linked_invoice_id_xml
                )
                if len(rc_invoice) == 1:
                    rc_invoice.fatturapa_attachment_in_id = attachment
        return attachments
