# Copyright 2021 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(
        env,
        [
            (
                "withholding.tax",
                "withholding_tax",
                "causale_pagamento_id",
                "payment_reason_id",
            ),
        ],
    )

    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "l10n_it_withholding_tax_causali.view_withholding_tax_form_causale",
                "l10n_it_withholding_tax_causali.view_withholding_tax_form_reason",
            ),
        ],
    )
