#  Copyright 2019 Simone Rubino - Agile Business Group
#  Copyright 2019 Lorenzo Battistini - TAKOBI
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Portale clienti",
    "summary": "Controlli per la fattura elettronica nel portale vendite",
    "version": "12.0.1.1.1",
    "author": "Odoo Community Association (OCA)",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_website_portal_fatturapa_sale",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_website_portal_fatturapa",
        "sale_management",
        "payment",
        "portal",
    ],
    "data": [
        "views/assets.xml",
        "views/payment_templates.xml",
        "views/res_config_settings_view.xml",
    ],
    "auto_install": True,
}
