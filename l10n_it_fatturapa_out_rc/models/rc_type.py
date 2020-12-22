from odoo import models, fields


class AccountRCType(models.Model):
    _inherit = "account.rc.type"

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Fiscal Document Type",
        help="To be used when sending self invoices to the exchange system")
