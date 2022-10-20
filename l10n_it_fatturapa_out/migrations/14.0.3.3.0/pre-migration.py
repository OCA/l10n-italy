#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

merged_modules = {
    "l10n_it_corrispettivi_fatturapa_out": "l10n_it_fatturapa_out",
}


def migrate(cr, installed_version):
    installed_merged_modules = {
        old_module: new_module
        for old_module, new_module in merged_modules.items()
        if openupgrade.is_module_installed(cr, old_module)
    }
    openupgrade.update_module_names(
        cr,
        installed_merged_modules.items(),
        merge_modules=True,
    )
