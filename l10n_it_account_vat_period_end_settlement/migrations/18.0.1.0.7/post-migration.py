#  Copyright 2026 Sergio Corato <https://github.com/sergiocorato>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_account_vat_period_end_settlement import hooks


@openupgrade.migrate()
def migrate(env, version):
    # Support Openupgrade with rename done with apriori.py
    hooks.post_absorb_old_module(env)
