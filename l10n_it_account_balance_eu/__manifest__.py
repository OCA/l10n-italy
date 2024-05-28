# Copyright 2022 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2022 MKT Srl (<www.mkt.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# last update: 2023-05-23

{
    "name": "ITA - Bilancio UE con XBRL",
    "version": "14.0.1.0.1",
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
    "data": [
        "data/account.balance.eu.csv",
        "data/account_balance_eu_reclassification.xml",
        "report/templates/layouts.xml",
        "report/account_balance_eu_report.xml",
        "security/account_balance_eu.xml",
        "views/account_balance_eu_view.xml",
        "views/report_template.xml",
        "wizards/account_balance_eu_wizard.xml",
    ],
    "qweb": ["static/src/xml/report.xml"],
    "application": False,
    "installable": True,
}
