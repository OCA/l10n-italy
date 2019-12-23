# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountType(models.Model):
    _inherit = 'account.account.type'

    # This field is almost equal to `internal_group`; yet, we wanna keep the
    # report independent from Odoo's accounting workflow, so we'll use this
    # new field for the report
    account_balance_report_section = fields.Selection(
        [('assets', "Assets"),
         ('expenses', "Expenses"),
         ('incomes', "Incomes"),
         ('liabilities', "Liabilities")],
        string="Account Balance Report - Section"
    )
