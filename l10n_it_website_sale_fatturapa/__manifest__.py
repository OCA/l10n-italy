# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italian Localization - Fattura Elettronica - eCommerce",
    "summary": "Aggiunge i campi necessari alla fatturazione elettronica "
               "nel form del checkout",
    "version": "12.0.1.0.3",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_website_sale_fatturapa",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa",
        "l10n_it_website_sale_fiscalcode"
    ],
    "data": [
        "views/templates.xml"
    ],
    "auto_install": True,
}
