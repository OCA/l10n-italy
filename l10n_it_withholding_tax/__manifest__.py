# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2019 Giovanni - GSLabIt
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Ritenute d'acconto",
    "version": "14.0.1.1.3",
    "category": "Account",
    "author": "Openforce, Odoo Italia Network, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_fatturapa",
    ],
    "data": [
        "views/account.xml",
        "views/withholding_tax.xml",
        "views/report_invoice.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
    ],
    "qweb": [
        "static/src/xml/account_payment.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}
