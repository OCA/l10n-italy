# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def pre_absorb_old_module(env):
    if openupgrade.is_module_installed(env.cr, "l10n_it_vat_statement_communication"):
        openupgrade.update_module_names(
            env.cr,
            [
                (
                    "l10n_it_vat_statement_communication",
                    "l10n_it_vat_settlement_communication",
                ),
            ],
            merge_modules=True,
        )
