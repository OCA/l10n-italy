from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    related_document_ids = fields.One2many(
        "account.move.related_document",
        "invoice_line_id",
        "Related Documents",
        copy=False,
    )
