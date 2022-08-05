#  Copyright 2021 Lorenzo Battistini @ TAKOBI
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Buoni pasto e registratore telematico",
    "version": "12.0.1.1.0",
    "category": "Point of Sale",
    "summary": "Consente di controllare e comunicare al registratore telematico le "
               "informazioni relative ai ticket",
    "author": "TAKOBI, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/fiscal_epos_print_meal_voucher",
    "maintainers": ["eLBati"],
    "depends": [
        "fiscal_epos_print",
        "pos_meal_voucher",
    ],
    "auto_install": True,
    "data": [
        "views/assets.xml",
        "views/account_views.xml",
        "views/pos_config_views.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
}
