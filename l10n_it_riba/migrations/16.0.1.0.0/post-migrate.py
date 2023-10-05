#  Copyright 2023 Simone Rubino - AionTech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

NEW_MODULE_NAME = "l10n_it_riba"


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr,
        NEW_MODULE_NAME,
        "migrations/16.0.1.0.0/data/noupdate.xml",
    )
    # TODO selection keys of riba.distinta[.line].state have changed
