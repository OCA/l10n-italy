# Copyright (C) 2026 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_intrastat"
NEW_MODULE_NAME = "l10n_it_intrastat_oca"


def _is_oca_version(env):
    env.cr.execute(
        """
            SELECT 1
            FROM ir_model_data
            WHERE
                module = %s
                AND model = %s
                AND name = %s
            LIMIT 1
        """,
        (OLD_MODULE_NAME, "report.intrastat.code", "intrastat_category_2014_01012100"),
    )
    return bool(env.cr.fetchone())


def pre_absorb_old_module(env):
    if not openupgrade.is_module_installed(env.cr, OLD_MODULE_NAME):
        return

    if _is_oca_version(env):
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
