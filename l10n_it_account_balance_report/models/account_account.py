# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Account(models.Model):
    _inherit = 'account.account'

    # This field is almost equal to `internal_group`; yet, we wanna keep the
    # report independent from Odoo's accounting workflow, so we'll use this
    # new field for the report
    account_balance_report_section = fields.Selection(
        [('assets', "Assets"),
         ('expenses', "Expenses"),
         ('incomes', "Incomes"),
         ('liabilities', "Liabilities")],
        readonly=True,
        related='user_type_id.account_balance_report_section',
        string="Account Balance Report - Section"
    )
