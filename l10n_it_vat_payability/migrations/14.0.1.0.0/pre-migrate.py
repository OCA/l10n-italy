# Copyright 2020 Sergio Zanchetta <https://github.com/primes2h>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.update_module_names(
        env.cr,
        [
            ("l10n_it_esigibilita_iva", "l10n_it_vat_payability"),
        ],
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "l10n_it_esigibilita_iva.view_tax_code_esigibilita_form",
                "l10n_it_vat_payability.view_tax_code_payability_form",
            ),
        ],
    )
