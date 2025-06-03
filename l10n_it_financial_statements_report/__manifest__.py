# Copyright 2019 Openforce (http://www.openforce.it)
# Copyright 2019 Alessandro Camilli (alessandrocamilli@openforce.it)
# Copyright 2019 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# Copyright 2025 Michele Di Croce - Stesi Consulting Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Stato patrimoniale e conto economico",
    "summary": "Rendicontazione .pdf e .xls per stato patrimoniale e conto"
    " economico a sezioni contrapposte",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Odoo Community Association (OCA), Openforce",
    "website": "https://github.com/OCA/l10n-italy",
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
}
