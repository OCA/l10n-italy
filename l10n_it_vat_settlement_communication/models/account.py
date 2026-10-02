from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    vsc_exclude_active_operation = fields.Boolean(
        string="Exclude from active operations"
    )
    vsc_exclude_passive_operation = fields.Boolean(
        string="Exclude from passive operations"
    )

    vsc_exclude_vat = fields.Boolean(string="Exclude from VAT payable / deducted")
