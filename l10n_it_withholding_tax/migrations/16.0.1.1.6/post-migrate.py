#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, installed_version):
    env.ref("l10n_it_withholding_tax.document_tax_totals_wt").mode = "extension"
