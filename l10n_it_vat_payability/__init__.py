# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# Copyright 2021 Alex Comba - Agile Business Group

from . import models

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_esigibilita_iva"):
        return

    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_esigibilita_iva.view_tax_code_esigibilita_form",
                "l10n_it_vat_payability.view_tax_code_payability_form",
            ),
        ],
    )
    openupgrade.update_module_names(
        cr,
        [
            ("l10n_it_esigibilita_iva", "l10n_it_vat_payability"),
        ],
        merge_modules=True,
    )
