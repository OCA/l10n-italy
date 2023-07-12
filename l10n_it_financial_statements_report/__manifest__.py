# Copyright 2019 Openforce (http://www.openforce.it)
# Copyright 2019 Alessandro Camilli (alessandrocamilli@openforce.it)
# Copyright 2019 Silvio Gregorini (silviogregorini@openforce.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Stato patrimoniale e conto economico",
    "summary": "Rendicontazione .pdf e .xls per stato patrimoniale e conto"
    " economico a sezioni contrapposte",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Odoo Community Association (OCA), Openforce",
    "website": "https://github.com/OCA/l10n-italy"
    "/tree/14.0/l10n_it_financial_statements_report",
    "license": "AGPL-3",
    "depends": [
        "account_financial_report",
        "account_menu",
        "l10n_it_account",
    ],
    "data": [
        "data/account_type.xml",
        "report/templates/financial_statements_report.xml",
        "report/reports.xml",
        "views/account_types.xml",
        "views/assets.xml",
        "wizard/wizard_financial_statements_report.xml",
    ],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "pre_init_hook": "pre_absorb_old_module",
    "installable": True,
}
