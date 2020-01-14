from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    fpdeptax = fields.Char(
        'Department on fiscal printer 1~99',
        size=1, default="1"
    )
