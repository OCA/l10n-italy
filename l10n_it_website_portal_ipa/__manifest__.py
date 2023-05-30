#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Codice IPA - Portale",
    "summary": "Aggiunge l'indice PA (IPA) tra i dettagli dell'utente nel portale.",
    "version": "16.0.1.0.1",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_ipa",
        "portal",
    ],
    "data": [
        "views/portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "l10n_it_website_portal_ipa/static/src/js/l10n_it_website_portal_ipa.js",
        ],
    },
    "auto_install": True,
}
