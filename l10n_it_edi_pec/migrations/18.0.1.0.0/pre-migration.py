# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_edi_pec import _l10n_it_edi_pec_pre_init_hook


@openupgrade.migrate()
def migrate(env, version):
    # Used by OpenUpgrade when module is in `apriori`
    _l10n_it_edi_pec_pre_init_hook(env)
