#  Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    # "Other Expenses" accounts got no section before 19.0.1.0.1;
    # sections set manually are kept
    env = api.Environment(cr, SUPERUSER_ID, {})
    accounts = env["account.account"].search(
        [
            ("account_type", "=", "expense_other"),
            ("financial_statements_report_section", "=", False),
        ]
    )
    accounts._compute_financial_statements_report_section()
