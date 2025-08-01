#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openupgradelib import openupgrade

from odoo.addons.l10n_it_currency_rate_update_boi import hooks


@openupgrade.migrate()
def migrate(env, version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.pre_absorb_old_module(env)
