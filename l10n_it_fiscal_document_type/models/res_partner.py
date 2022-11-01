from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    out_fiscal_document_type = fields.Many2one(
        "fiscal.document.type",
    )
    in_fiscal_document_type = fields.Many2one(
        "fiscal.document.type",
    )
