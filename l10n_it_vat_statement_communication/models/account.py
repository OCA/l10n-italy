from openerp import fields, models


class AccountTaxCode(models.Model):
    _inherit = "account.tax.code"

    vsc_exclude_operation = fields.Boolean(
        string='Exclude from active / passive operations')

    vsc_exclude_vat = fields.Boolean(
        string='Exclude from VAT payable / deducted')
