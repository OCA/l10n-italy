
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_set_deferred_invoice_type = fields.Boolean(
        string="Automatically set document type for deferred invoices",
        default=True,
        help="If set, TD24 document type code will be applied to invoices created "
             "from transport document")


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_set_deferred_invoice_type = fields.Boolean(
        related="company_id.auto_set_deferred_invoice_type", readonly=False)
