#  Copyright 2021 Marco Colombo (<https://github/TheMule71)
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Data competenza IVA",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Settlement date for VAT Statement",
    "license": "AGPL-3",
    "author": "Marco Colombo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy"
    "/tree/16.0/l10n_it_vat_settlement_date",
    "depends": [
        "account",
        "account_tax_balance",
        "account_vat_period_end_statement",
        "l10n_it_vat_registries",
    ],
    "data": [
        "views/account_move_views.xml",
        "reports/report_registro_iva.xml",
    ],
}
