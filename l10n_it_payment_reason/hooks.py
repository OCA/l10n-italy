from openupgradelib import openupgrade


def module_migration(cr):
    if openupgrade.is_module_installed(cr, "l10n_it_causali_pagamento"):
        openupgrade.rename_xmlids(
            cr,
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

        openupgrade.update_module_names(
            cr,
            [
                ("l10n_it_causali_pagamento", "l10n_it_payment_reason"),
            ],
            merge_modules=True,
        )

        openupgrade.rename_models(
            cr,
            [
                ("causale.pagamento", "payment.reason"),
            ],
        )

        openupgrade.rename_tables(
            cr,
            [
                ("causale_pagamento", "payment_reason"),
            ],
        )
