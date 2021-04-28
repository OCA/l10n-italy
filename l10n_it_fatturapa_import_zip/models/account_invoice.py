from odoo import fields, models


class Invoice(models.Model):
    _inherit = "account.move"

    attachment_out_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-bills ZIP import",
        readonly=True,
        related="fatturapa_attachment_out_id.attachment_import_zip_id",
        store=True,
    )
    attachment_in_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-invoices ZIP import",
        readonly=True,
        related="fatturapa_attachment_in_id.attachment_import_zip_id",
        store=True,
    )
