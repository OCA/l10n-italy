from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api

from . import models


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

    env = api.Environment(cr, SUPERUSER_ID, {})
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
