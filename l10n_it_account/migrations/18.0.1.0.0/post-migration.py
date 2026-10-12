from odoo import SUPERUSER_ID, api

from odoo.addons.l10n_it_account.migration_tools import (
    _remove_module,
    remove_modules_views,
)

# Old OCA modules superseded in v18: split payment and reverse charge are now
# handled by Odoo core (l10n_it / account). We migrate no data for them here --
# we only drop their now-dangling views and uninstall them.
OLD_MODULES_TO_REMOVE = [
    "l10n_it_reverse_charge_start_end_dates",
    "l10n_it_reverse_charge",
    "l10n_it_split_payment",
]


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    remove_modules_views(cr, OLD_MODULES_TO_REMOVE)
    for module in OLD_MODULES_TO_REMOVE:
        _remove_module(env, module)
