#  Copyright 2025 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.addons.l10n_it_account_vat_period_end_settlement import hooks


def migrate(cr, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.migrate_old_module(cr)
