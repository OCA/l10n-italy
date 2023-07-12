#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_financial_statements_report import hooks


def migrate(cr, installed_version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.migrate_old_module(cr)
