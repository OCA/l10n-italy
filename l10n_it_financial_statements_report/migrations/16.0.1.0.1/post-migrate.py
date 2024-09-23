#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    prepayment_accounts = env["account.account"].search(
        [
            ("account_type", "=", "asset_prepayments"),
        ],
    )
    prepayment_accounts._compute_financial_statements_report_section()
