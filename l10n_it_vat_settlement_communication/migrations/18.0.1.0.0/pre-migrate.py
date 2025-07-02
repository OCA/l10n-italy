#  Copyright 2025 Lorenzo Battistini
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.l10n_it_account_vat_period_end_settlement import hooks


def migrate(env, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.pre_absorb_old_module(env)
