# Copyright 2019 Simone Rubino
# Copyright 2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italian Localization - Fattura elettronica - Portale",
    "summary": "Add fatturapa fields and checks in frontend user's details",
    "version": "12.0.1.3.0",
    "author": "Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_website_portal_fatturapa",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa",
        "l10n_it_website_portal_fiscalcode",
        "l10n_it_website_portal_ipa",
    ],
    "data": [
        "views/l10n_it_website_portal_fatturapa_templates.xml"
    ],
    "auto_install": True,
}
