# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, "assets_management"):
        openupgrade.update_module_names(
            cr,
            [
                ("assets_management", "l10n_it_asset_management"),
            ],
            merge_modules=True,
        )
