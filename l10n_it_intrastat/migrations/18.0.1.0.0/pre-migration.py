#  Copyright 2025 Alex Comba - Agile Business Group
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade
from openupgradelib.openupgrade_tools import column_exists


@openupgrade.migrate()
def migrate(env, version):
    table = "account_fiscal_position"
    column = "intrastat"
    new_column = "l10n_it_oca_intrastat"
    if column_exists(env.cr, table, column):
        openupgrade.rename_fields(
            env,
            [
                (
                    "account.fiscal.position",
                    table,
                    column,
                    new_column,
                )
            ],
        )
