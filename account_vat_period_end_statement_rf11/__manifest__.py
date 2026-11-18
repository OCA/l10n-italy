# Copyright 2024 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Supporto IVA 74-ter - Liquidazione IVA",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "summary": "Supporto IVA secondo art.74-ter, DPR 633/72 - Agenzie viaggi e turismo per la liquidazione IVA",
    "author": "Innovyou, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "maintainers": ["eLBati", "LorenzoC0"],
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_tax_balance",
        "account_vat_period_end_statement"
    ],
    "data": [
        "views/account_tax_views.xml",
        "views/account_vat_period_end_views.xml",
        "report/report_vatperiodendstatement.xml",
    ],
    "installable": True,
}
