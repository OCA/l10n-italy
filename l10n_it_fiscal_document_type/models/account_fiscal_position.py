from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    fiscal_document_type_id = fields.Many2one(
        "fiscal.document.type", string="Fiscal Document Type", readonly=False
    )
