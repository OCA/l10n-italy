from . import models

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_causali_pagamento"):
        return

    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_causali_pagamento.a",
                "l10n_it_causali_pagamento.b",
                "l10n_it_causali_pagamento.c",
                "l10n_it_causali_pagamento.d",
                "l10n_it_causali_pagamento.e",
                "l10n_it_causali_pagamento.g",
                "l10n_it_causali_pagamento.h",
                "l10n_it_causali_pagamento.i",
                "l10n_it_causali_pagamento.l",
                "l10n_it_causali_pagamento.m",
                "l10n_it_causali_pagamento.n",
                "l10n_it_causali_pagamento.o",
                "l10n_it_causali_pagamento.p",
                "l10n_it_causali_pagamento.q",
                "l10n_it_causali_pagamento.r",
                "l10n_it_causali_pagamento.s",
                "l10n_it_causali_pagamento.t",
                "l10n_it_causali_pagamento.u",
                "l10n_it_causali_pagamento.v",
                "l10n_it_causali_pagamento.w",
                "l10n_it_causali_pagamento.x",
                "l10n_it_causali_pagamento.y",
                "l10n_it_causali_pagamento.z",
                "l10n_it_causali_pagamento.l1",
                "l10n_it_causali_pagamento.m1",
                "l10n_it_causali_pagamento.m2",
                "l10n_it_causali_pagamento.o1",
                "l10n_it_causali_pagamento.v1",
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
