# Copyright 2018 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Integrazione bollo",
    "summary": "Modulo ponte tra emissione fatture elettroniche e imposta di bollo",
    "version": "17.5.0.0.1",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "auto_install": True,
    "depends": [
        "l10n_it_account_stamp",
        "l10n_it_edi",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
}
