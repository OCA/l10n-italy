from odoo import _, fields, models, api
from odoo.exceptions import ValidationError
import re

regex = r"^[1-9][0-9]?$"  # regular expression to match numbers between [1 - 99]


class AccountTax(models.Model):
    _inherit = 'account.tax'

    fpdeptax = fields.Char(
        'Department on fiscal printer 1~99',
        size=2, default="1"
    )

    @api.constrains('fpdeptax')
    def _validate_fpdeptax(self):
        for tax in self:
            if not re.search(regex, tax.fpdeptax):
                raise ValidationError(_("Department ID number range [1 - 99]"))
