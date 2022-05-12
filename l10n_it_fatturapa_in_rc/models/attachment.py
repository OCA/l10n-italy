from odoo import models, api


class Attachment(models.Model):
    _inherit = "fatturapa.attachment.in"

    @api.model
    def create(self, vals):
        attachment = super(Attachment, self).create(vals)
        if attachment.linked_invoice_id_xml and attachment.is_self_invoice:
            rc_invoice = self.env["account.invoice"].search([
                ("type", "in", ("in_invoice", "in_refund")),
                ("rc_self_invoice_id", "!=", False),
                ("number", "=", attachment.linked_invoice_id_xml)
            ], limit=1)
            rc_invoice.fatturapa_attachment_in_id = attachment.id
        return attachment
