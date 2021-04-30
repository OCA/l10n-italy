# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(
        env.cr,
        [
            ("faturapa.activity.progress", "fatturapa.activity.progress"),
            ("faturapa.summary.data", "fatturapa.summary.data"),
        ],
    )
    openupgrade.rename_tables(
        env.cr,
        [
            ("faturapa_activity_progress", "fatturapa_activity_progress"),
            ("faturapa_summary_data", "fatturapa_summary_data"),
        ],
    )
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "l10n_it_fatturapa.account.account_payment_term",
                "l10n_it_fatturapa.account.account_payment_term_immediate",
            ),
            ("l10n_it_fatturapa.invoice_form", "l10n_it_fatturapa.view_move_form"),
            (
                "l10n_it_fatturapa.view_invoice_line_form_fatturapa",
                "l10n_it_fatturapa.view_invoice_form_fatturapa",
            ),
        ],
    )
