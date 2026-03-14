# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

from odoo.addons.l10n_it_account.migration_tools import remove_modules_views

_logger = logging.getLogger(__name__)

_OLD_MODULES = [
    "l10n_it_vat_registries_rc",
    "l10n_it_vat_registries_split_payment",
]


@openupgrade.migrate()
def migrate(env, version):
    for module in _OLD_MODULES:
        if openupgrade.is_module_installed(env.cr, module):
            _logger.info(
                "Module %s was installed in previous version, removing its views",
                module,
            )
            remove_modules_views(env.cr, module)
            openupgrade.update_module_names(
                env.cr,
                [(module, "l10n_it_vat_registries")],
                merge_modules=True,
            )
