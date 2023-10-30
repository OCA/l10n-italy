# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_codici_carica"
NEW_MODULE_NAME = "l10n_it_appointment_code"


def rename_old_italian_module(cr):
    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_appointment_code.view_codice_carica_tree",
                "l10n_it_appointment_code.view_appointment_code_tree",
            ),
            (
                "l10n_it_appointment_code.view_codice_carica_form",
                "l10n_it_appointment_code.view_appointment_code_form",
            ),
            (
                "l10n_it_appointment_code.action_codice_carica",
                "l10n_it_appointment_code.action_appointment_code",
            ),
            (
                "l10n_it_appointment_code.menu_codice_carica",
                "l10n_it_appointment_code.menu_appointment_code",
            ),
        ],
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
