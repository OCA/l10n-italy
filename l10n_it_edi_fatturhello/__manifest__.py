# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Fattura elettronica - Supporto Fatturhello",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Invio e ricezione fatture elettroniche tramite Fatturhello",
    "author": "PyTech, Odoo Community Association (OCA)",
    "maintainers": [
        "HekkiMelody",
        "SirPyTech",
    ],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi_sdi",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/login_views.xml",
    ],
}
