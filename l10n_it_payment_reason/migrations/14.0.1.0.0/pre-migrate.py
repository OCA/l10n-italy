# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_payment_reason import hooks


@openupgrade.migrate()
def migrate(env, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    if not installed_version:
        return
    hooks.rename_old_italian_module(env.cr)
