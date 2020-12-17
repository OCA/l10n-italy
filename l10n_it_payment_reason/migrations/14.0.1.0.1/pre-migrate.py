# Copyright 2020 Sergio Zanchetta <https://github.com/primes2h>
# Copyright 2021 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.update_module_names(
        env.cr,
        [
            ("l10n_it_causali_pagamento", "l10n_it_payment_reason"),
        ],
    )
    openupgrade.rename_models(
        env.cr,
        [
            ("causale.pagamento", "payment.reason"),
        ],
    )
    openupgrade.rename_tables(
        env.cr,
        [
            ("causale.pagamento", "payment.reason"),
        ],
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "l10n_it_causali_pagamento.view_causale_pagamento_tree",
                "l10n_it_payment_reason.view_payment_reason_tree",
            ),
            (
                "l10n_it_causali_pagamento.view_causale_pagamento_form",
                "l10n_it_payment_reason.view_payment_reason_form",
            ),
            (
                "l10n_it_causali_pagamento.action_causale_pagamento",
                "l10n_it_payment_reason.action_payment_reason",
            ),
            (
                "l10n_it_causali_pagamento.menu_causale_pagamento",
                "l10n_it_payment_reason.menu_payment_reason",
            ),
        ],
    )
