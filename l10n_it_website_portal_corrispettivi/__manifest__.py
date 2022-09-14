# Copyright 2021 Lorenzo Battistini @  TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Ricevute - Portale",
    "summary": "Aggiunge ricevuta o fattura come opzione nel profilo dell'utente"
               " portale",
    "version": "12.0.1.0.0",
    "author": "Odoo Community Association (OCA), TAKOBI",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_website_portal_corrispettivi",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_corrispettivi",
        "portal"
    ],
    "data": [
        "views/l10n_it_website_portal_corrispettivi_templates.xml"
    ],
    "auto_install": True,
}
