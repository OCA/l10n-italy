#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    # Assign the sign of the account type to the account
    openupgrade.logged_query(
        cr,
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
