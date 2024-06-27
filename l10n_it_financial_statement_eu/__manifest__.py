# Copyright 2022 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2022 MKT Srl (<www.mkt.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# last update: 2023-05-23

{
    "name": "ITA - Bilancio UE con XBRL",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "MKT Srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "maintainers": ["mktsrl"],
    "depends": [
        "account",
        "date_range",
        "l10n_it_rea",
        "l10n_it_fiscalcode",
        "report_xlsx",
        "report_xml",
    ],
    "assets": {
        "web.assets_backend": [
            "l10n_it_financial_statement_eu/static/src/js/client_action.esm.js",
            "l10n_it_financial_statement_eu/static/src/xml/report.xml",
        ],
    },
    "data": [
        "security/financial_statement_eu_security.xml",
        "data/financial.statement.eu.csv",
        "report/templates/layouts.xml",
        "report/financial_statement_eu_report.xml",
        "views/financial_statement_eu_view.xml",
        "wizard/financial_statement_eu_wizard.xml",
    ],
    "application": False,
    "installable": True,
    "post_init_hook": "_l10n_it_financial_statement_eu_post_init",
}
