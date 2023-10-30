# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# Copyright 2021 Alex Comba - Agile Business Group
from openupgradelib import openupgrade

from odoo.tools import DotDict

OLD_MODULE_NAME = "l10n_it_withholding_tax_causali"
NEW_MODULE_NAME = "l10n_it_withholding_tax_reason"


def rename_old_italian_module(cr):
    # module reference in xmlids are already renamed from update_module_names()
    openupgrade.rename_xmlids(
        cr,
        [
            (
                ".".join((NEW_MODULE_NAME, "view_withholding_tax_form_causale")),
                ".".join((NEW_MODULE_NAME, "view_withholding_tax_form_reason")),
            ),
        ],
    )

    old_payment_reason = "causale_pagamento_id"
    new_payment_reason = "payment_reason_id"
    if not openupgrade.column_exists(cr, "account_move_line", new_payment_reason):
        openupgrade.rename_fields(
            # The method only needs the cursor, not the whole Environment
            DotDict(
                cr=cr,
            ),
            [
                (
                    "withholding.tax",
                    "withholding_tax",
                    old_payment_reason,
                    new_payment_reason,
                ),
            ],
            # Prevent Environment usage whenever it will be implemented.
            no_deep=True,
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
