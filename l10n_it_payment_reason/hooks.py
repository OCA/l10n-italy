# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_causali_pagamento"):
        return

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
            ("l10n_it_causali_pagamento.a", "l10n_it_payment_reason.a"),
            ("l10n_it_causali_pagamento.b", "l10n_it_payment_reason.b"),
            ("l10n_it_causali_pagamento.c", "l10n_it_payment_reason.c"),
            ("l10n_it_causali_pagamento.d", "l10n_it_payment_reason.d"),
            ("l10n_it_causali_pagamento.e", "l10n_it_payment_reason.e"),
            ("l10n_it_causali_pagamento.g", "l10n_it_payment_reason.g"),
            ("l10n_it_causali_pagamento.h", "l10n_it_payment_reason.h"),
            ("l10n_it_causali_pagamento.i", "l10n_it_payment_reason.i"),
            ("l10n_it_causali_pagamento.l", "l10n_it_payment_reason.l"),
            ("l10n_it_causali_pagamento.m", "l10n_it_payment_reason.m"),
            ("l10n_it_causali_pagamento.n", "l10n_it_payment_reason.n"),
            ("l10n_it_causali_pagamento.o", "l10n_it_payment_reason.o"),
            ("l10n_it_causali_pagamento.p", "l10n_it_payment_reason.p"),
            ("l10n_it_causali_pagamento.q", "l10n_it_payment_reason.q"),
            ("l10n_it_causali_pagamento.r", "l10n_it_payment_reason.r"),
            ("l10n_it_causali_pagamento.s", "l10n_it_payment_reason.s"),
            ("l10n_it_causali_pagamento.t", "l10n_it_payment_reason.t"),
            ("l10n_it_causali_pagamento.u", "l10n_it_payment_reason.u"),
            ("l10n_it_causali_pagamento.v", "l10n_it_payment_reason.v"),
            ("l10n_it_causali_pagamento.w", "l10n_it_payment_reason.w"),
            ("l10n_it_causali_pagamento.x", "l10n_it_payment_reason.x"),
            ("l10n_it_causali_pagamento.y", "l10n_it_payment_reason.y"),
            ("l10n_it_causali_pagamento.z", "l10n_it_payment_reason.z"),
            ("l10n_it_causali_pagamento.l1", "l10n_it_payment_reason.l1"),
            ("l10n_it_causali_pagamento.m1", "l10n_it_payment_reason.m1"),
            ("l10n_it_causali_pagamento.m2", "l10n_it_payment_reason.m2"),
            ("l10n_it_causali_pagamento.o1", "l10n_it_payment_reason.o1"),
            (
                "l10n_it_causali_pagamento.v1",
                "l10n_it_payment_reason.v1",
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
