# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_codici_carica"):
        return

    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_codici_carica.view_codice_carica_tree",
                "l10n_it_appointment_code.view_appointment_code_tree",
            ),
            (
                "l10n_it_codici_carica.view_codice_carica_form",
                "l10n_it_appointment_code.view_appointment_code_form",
            ),
            (
                "l10n_it_codici_carica.action_codice_carica",
                "l10n_it_appointment_code.action_appointment_code",
            ),
            (
                "l10n_it_codici_carica.menu_codice_carica",
                "l10n_it_appointment_code.menu_appointment_code",
            ),
            ("l10n_it_codici_carica.1", "l10n_it_appointment_code.1"),
            ("l10n_it_codici_carica.2", "l10n_it_appointment_code.2"),
            ("l10n_it_codici_carica.3", "l10n_it_appointment_code.3"),
            ("l10n_it_codici_carica.4", "l10n_it_appointment_code.4"),
            ("l10n_it_codici_carica.5", "l10n_it_appointment_code.5"),
            ("l10n_it_codici_carica.6", "l10n_it_appointment_code.6"),
            ("l10n_it_codici_carica.7", "l10n_it_appointment_code.7"),
            ("l10n_it_codici_carica.8", "l10n_it_appointment_code.8"),
            ("l10n_it_codici_carica.9", "l10n_it_appointment_code.9"),
            ("l10n_it_codici_carica.10", "l10n_it_appointment_code.10"),
            ("l10n_it_codici_carica.11", "l10n_it_appointment_code.11"),
            ("l10n_it_codici_carica.12", "l10n_it_appointment_code.12"),
            ("l10n_it_codici_carica.13", "l10n_it_appointment_code.13"),
            ("l10n_it_codici_carica.14", "l10n_it_appointment_code.14"),
            ("l10n_it_codici_carica.15", "l10n_it_appointment_code.15"),
        ],
    )
    openupgrade.update_module_names(
        cr,
        [
            ("l10n_it_codici_carica", "l10n_it_appointment_code"),
        ],
        merge_modules=True,
    )
    openupgrade.rename_models(
        cr,
        [
            ("codice.carica", "appointment.code"),
        ],
    )
    openupgrade.rename_tables(
        cr,
        [
            ("codice_carica", "appointment_code"),
        ],
    )
