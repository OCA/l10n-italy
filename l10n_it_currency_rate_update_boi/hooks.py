# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "currency_rate_update_boi"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "currency_rate_update_boi",
                    "l10n_it_currency_rate_update_boi",
                ),
            ],
            merge_modules=True,
        )
