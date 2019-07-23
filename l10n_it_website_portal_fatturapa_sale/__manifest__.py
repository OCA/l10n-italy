#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Portale clienti",
    "summary": "Controlli per la fattura elettronica nel portale vendite",
    "version": "12.0.1.0.1",
    "author": "Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy/tree/"
               "12.0/l10n_it_website_portal_fatturapa_sale",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_website_portal_fatturapa",
        "sale_management",
    ],
    "data": [
        "views/assets.xml",
        "views/payment_templates.xml",
    ],
    "auto_install": True,
}
