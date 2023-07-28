# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2019 Giovanni - GSLabIt
# Copyright 2022 Marco Colombo - <marco.colombo@phi.technology>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Ritenute d'acconto",
    "version": "16.0.1.1.2",
    "category": "Account",
    "author": "Openforce, Odoo Italia Network, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/account.xml",
        "views/withholding_tax.xml",
        "views/report_invoice.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "l10n_it_withholding_tax/static/src/components/**/*",
        ],
    },
    "installable": True,
    "development_status": "Beta",
}
