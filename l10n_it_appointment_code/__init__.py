from . import models

from openupgradelib import openupgrade


def rename_old_italian_module(cr):

    if not openupgrade.is_module_installed(cr, "l10n_it_codici_carica"):
        return

    openupgrade.rename_xmlids(
        cr,
        [
            (
                "l10n_it_codici_carica.1",
                "l10n_it_codici_carica.2",
                "l10n_it_codici_carica.3",
                "l10n_it_codici_carica.4",
                "l10n_it_codici_carica.5",
                "l10n_it_codici_carica.6",
                "l10n_it_codici_carica.7",
                "l10n_it_codici_carica.8",
                "l10n_it_codici_carica.9",
                "l10n_it_codici_carica.10",
                "l10n_it_codici_carica.11",
                "l10n_it_codici_carica.12",
                "l10n_it_codici_carica.13",
                "l10n_it_codici_carica.14",
                "l10n_it_codici_carica.15",
            ),
        ],
    )

    openupgrade.update_module_names(
        cr,
        [
            ("l10n_it_codici_carica", "l10n_it_appointment_code"),
        ],
        merge_modules=True,
    )
