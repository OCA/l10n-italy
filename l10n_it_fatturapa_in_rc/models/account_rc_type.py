from odoo import fields, models


class RCType(models.Model):
    _inherit = "account.rc.type"

    e_invoice_suppliers = fields.Boolean(
        "E-invoice suppliers",
        help="Automatically used when importing e-invoices from Italian " "suppliers",
    )
