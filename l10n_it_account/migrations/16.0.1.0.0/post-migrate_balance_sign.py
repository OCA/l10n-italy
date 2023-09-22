#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, installed_version):
    # Assign the sign of the account type to the account
    if openupgrade.table_exists(env.cr, "account_account_type"):
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE account_account
            SET
                account_balance_sign = aat.account_balance_sign
            FROM
                account_account_type aat
            WHERE
                aat.id = account_account.user_type_id
            """,
        )
    else:
        env["account.account"].set_account_types_negative_sign()
