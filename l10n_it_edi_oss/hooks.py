# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_old_module = "l10n_it_fatturapa_out_oss"
_new_module = "l10n_it_edi_oss"


def pre_absorb_old_module(env):
    cr = env.cr
    if openupgrade.is_module_installed(cr, _old_module):
        openupgrade.update_module_names(
            cr, [(_old_module, _new_module)], merge_modules=True
        )
