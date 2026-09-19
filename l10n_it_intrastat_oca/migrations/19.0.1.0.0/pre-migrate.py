# Copyright (C) 2026 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_intrastat_oca import hooks


@openupgrade.migrate()
def migrate(env, version):
    # Used by OpenUpgrade when module is in `apriori`
    hooks.pre_absorb_old_module(env)
