# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_ricevute_bancarie"
NEW_MODULE_NAME = "l10n_it_riba"


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "l10n_it_riba"):
        openupgrade.update_module_names(
            env.cr,
            [
                ("l10n_it_riba", "l10n_it_riba_oca"),
            ],
            merge_modules=True,
        )
