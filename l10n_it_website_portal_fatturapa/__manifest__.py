# Copyright 2019 Simone Rubino
# Copyright 2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italian Localization - Fattura elettronica - Portale",
    "summary": "Add fatturapa fields and checks in frontend user's details",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
    "/tree/16.0/l10n_it_website_portal_fatturapa",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa",
        "l10n_it_website_portal_fiscalcode",
        "l10n_it_website_portal_ipa",
    ],
    "data": ["views/l10n_it_website_portal_fatturapa_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "l10n_it_website_portal_fatturapa/static/"
            "src/js/l10n_it_website_portal_fatturapa.js",
        ],
    },
    "auto_install": True,
}
