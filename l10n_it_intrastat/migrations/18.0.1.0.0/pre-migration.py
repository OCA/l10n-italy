#  Copyright 2025 Alex Comba - Agile Business Group
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "account.fiscal.position",
                "account.fiscal.position",
                "intrastat",
                "l10n_it_oca_intrastat",
            )
        ],
    )
