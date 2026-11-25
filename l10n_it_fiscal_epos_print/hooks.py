# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "fiscal_epos_print"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "fiscal_epos_print",
                    "l10n_it_fiscal_epos_print",
                ),
            ],
            merge_modules=True,
        )
