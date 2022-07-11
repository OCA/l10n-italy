# Copyright 2019 Openforce (http://www.openforce.it)
# Copyright 2019 Alessandro Camilli (alessandrocamilli@openforce.it)
# Copyright 2019 Silvio Gregorini (silviogregorini@openforce.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Stato patrimoniale e conto economico",
    "summary": "Rendicontazione .pdf per stato patrimoniale e conto"
    " economico a sezioni contrapposte",
    "version": "14.0.1.0.0+PR2860",
    "category": "Localisation/Italy",
    "author": "Odoo Community Association (OCA), Openforce",
    "website": "https://github.com/OCA/l10n-italy" "/l10n_it_account_balance_report",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_financial_report",
        "account_menu",
        "l10n_it_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/account_type.xml",
        "report/templates/account_balance_report.xml",
        "report/reports.xml",
        "views/action_client.xml",
        "views/account_types.xml",
        "wizard/wizard_account_balance_report.xml",
    ],
    "qweb": [
        "static/src/xml/report.xml",
    ],
    "installable": True,
}
