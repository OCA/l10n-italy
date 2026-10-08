# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_intrastat_statement"
NEW_MODULE_NAME = "l10n_it_intrastat_statement_oca"


def _is_oca_module_installed(cr, module):
    cr.execute(
        """
        SELECT 1
        FROM ir_module_module
        WHERE name = %s
            AND state IN ('installed', 'to upgrade')
            AND author LIKE %s
        """,
        (module, "%OCA%"),
    )
    return bool(cr.fetchone())


def pre_absorb_old_module(env):
    if _is_oca_module_installed(env.cr, OLD_MODULE_NAME):
        openupgrade.update_module_names(
            env.cr,
            [
                (OLD_MODULE_NAME, NEW_MODULE_NAME),
            ],
            merge_modules=True,
        )
