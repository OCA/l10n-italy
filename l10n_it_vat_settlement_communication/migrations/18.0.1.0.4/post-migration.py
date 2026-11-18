#  Copyright 2026 Sergio Corato <https://github.com/sergiocorato>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_vat_settlement_communication import hooks


@openupgrade.migrate()
def migrate(env, version):
    # do the same as pre-migration for post-migration
    hooks.post_absorb_old_module(env)
