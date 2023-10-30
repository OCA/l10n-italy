# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_causali_pagamento"
NEW_MODULE_NAME = "l10n_it_payment_reason"


def rename_old_italian_module(cr):
    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_payment_reason.view_causale_pagamento_tree",
                "l10n_it_payment_reason.view_payment_reason_tree",
            ),
            (
                "l10n_it_payment_reason.view_causale_pagamento_form",
                "l10n_it_payment_reason.view_payment_reason_form",
            ),
            (
                "l10n_it_payment_reason.action_causale_pagamento",
                "l10n_it_payment_reason.action_payment_reason",
            ),
            (
                "l10n_it_payment_reason.menu_causale_pagamento",
                "l10n_it_payment_reason.menu_payment_reason",
            ),
        ],
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


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, OLD_MODULE_NAME):
        openupgrade.update_module_names(
            cr,
            [
                (OLD_MODULE_NAME, NEW_MODULE_NAME),
            ],
            merge_modules=True,
        )
        rename_old_italian_module(cr)
