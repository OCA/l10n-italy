# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

OLD_MODULE = "l10n_it_riba"
NEW_MODULE = "l10n_it_riba_oca"


def _is_oca_module(cr, module):
    """Check if `module` is OCA."""
    cr.execute(
        """
SELECT
    id
FROM
    ir_module_module
WHERE
    name=%s
    AND author LIKE '%%OCA%%'
""",
        (module,),
    )
    return bool(cr.fetchone())


def _is_oca_module_installed(cr, module):
    """Check if `module` is installed and OCA."""
    return openupgrade.is_module_installed(cr, module) and _is_oca_module(cr, module)


@openupgrade.migrate()
def migrate(env, installed_version):
    if _is_oca_module_installed(env.cr, OLD_MODULE):
        # Delete the new module
        # because the list of modules has been updated
        # during the upgrade
        env["ir.module.module"].search([("name", "=", NEW_MODULE)]).unlink()
        openupgrade.update_module_names(
            env.cr,
            [
                (OLD_MODULE, NEW_MODULE),
            ],
        )
