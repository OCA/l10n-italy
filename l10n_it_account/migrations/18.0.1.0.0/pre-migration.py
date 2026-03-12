# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api

from odoo.addons.l10n_it_account.migration_tools import _remove_module

# Modules that no longer exist in v18 and whose features are not merged into any
# surviving module. They are flagged for removal (state = 'to remove') so that
# Odoo uninstalls them (data, fields, columns and views) at the end of the
# upgrade run, consistently with the other old modules removed via
# ``_remove_module``.
OLD_MODULES_TO_REMOVE = [
    "l10n_it_vat_statement_split_payment",
]


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in OLD_MODULES_TO_REMOVE:
        _remove_module(env, module)
