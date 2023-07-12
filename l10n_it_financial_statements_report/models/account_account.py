# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Account(models.Model):
    _inherit = "account.account"

    # This field is almost equal to `internal_group`; yet, we wanna keep the
    # report independent from Odoo's accounting workflow, so we'll use this
    # new field for the report
    financial_statements_report_section = fields.Selection(
        readonly=True,
        related="user_type_id.financial_statements_report_section",
        string="Financial Statements Report - Section",
    )
