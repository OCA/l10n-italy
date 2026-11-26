# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Bilancio di verifica senza registrazioni di chiusura",
    "summary": "Esclude le registrazioni di chiusura e apertura dell'esercizio "
    "da bilancio di verifica, stato patrimoniale e conto economico.",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "TAKOBI, LorenzoC0, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account_fiscal_year_closing",
        "l10n_it_financial_statements_report",
    ],
    "data": [
        "wizard/trial_balance_wizard_views.xml",
    ],
}
