#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Indice PA nel portale",
    "summary": "Aggiunge l'indice PA (IPA) "
               "tra i dettagli dell'utente nel portale.",
    "version": "12.0.1.1.1",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_website_portal_ipa",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_ipa",
        "portal",
    ],
    "data": [
        "views/portal_templates.xml",
    ],
    "auto_install": True,
}
