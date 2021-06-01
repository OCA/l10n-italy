# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Esigibilità IVA",
    "version": "14.0.1.0.2",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "author": "Openforce di Camilli Alessandro, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": [
        "account",
    ],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "data": [
        "views/account_view.xml",
    ],
    "installable": True,
    "pre_init_hook": "rename_old_italian_module",
}
