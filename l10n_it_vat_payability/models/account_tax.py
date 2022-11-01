# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    payability = fields.Selection(
        [
            ("I", "VAT payable immediately"),
            ("D", "unrealized VAT"),
            ("S", "split payments"),
        ],
        string="VAT payability",
    )
