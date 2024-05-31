# Copyright 2019 Openforce (http://www.openforce.it)
# Copyright 2019 Alessandro Camilli (alessandrocamilli@openforce.it)
# Copyright 2019 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Stato patrimoniale e conto economico",
    "summary": "Rendicontazione .pdf e .xls per stato patrimoniale e conto"
    " economico a sezioni contrapposte",
    "version": "16.0.1.0.2",
    "category": "Localization/Italy",
    "author": "Odoo Community Association (OCA), Openforce",
    "website": "https://github.com/OCA/l10n-italy"
    "/tree/16.0/l10n_it_financial_statements_report",
    "license": "AGPL-3",
    "depends": [
        "account_financial_report",
        "l10n_it_account",
    ],
    "data": [
        "report/templates/financial_statements_report.xml",
        "report/reports.xml",
        "wizard/wizard_financial_statements_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "l10n_it_financial_statements_report/static/src/js/action_manager_report.js",
            "l10n_it_financial_statements_report/static/src/js/client_action.js",
        ],
    },
}
