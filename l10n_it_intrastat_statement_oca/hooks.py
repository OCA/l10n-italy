# Copyright (C) 2026 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_intrastat_statement_oca"
NEW_MODULE_NAME = "l10n_it_intrastat_statement_oca"


def pre_absorb_old_module(env):
    if not openupgrade.is_module_installed(env.cr, OLD_MODULE_NAME):
        return

    openupgrade.update_module_names(
        env.cr,
        [
            (
                OLD_MODULE_NAME,
                NEW_MODULE_NAME,
            ),
        ],
        merge_modules=True,
    )
