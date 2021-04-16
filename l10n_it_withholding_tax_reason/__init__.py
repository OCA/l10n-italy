# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# Copyright 2021 Alex Comba - Agile Business Group

from . import models

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_withholding_tax_causali"):
        return

    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_withholding_tax_causali.view_withholding_tax_form_causale",
                "l10n_it_withholding_tax_causali.view_withholding_tax_form_reason",
            ),
        ],
    )

    openupgrade.update_module_names(
        cr,
        [
            ("l10n_it_withholding_tax_causali", "l10n_it_withholding_tax_reason"),
        ],
        merge_modules=True,
    )
