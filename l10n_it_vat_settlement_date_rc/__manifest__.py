#  Copyright 2021 Marco Colombo (<https://github/TheMule71)
#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Data competenza IVA e inversione contabile",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Use VAT Settlement Date in reverse charge.",
    "license": "AGPL-3",
    "author": "Marco Colombo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy"
    "/tree/16.0/l10n_it_vat_settlement_date_rc",
    "depends": [
        "account",
        "l10n_it_reverse_charge",
        "l10n_it_vat_settlement_date",
    ],
    "auto_install": True,
    "data": [
        "views/account_move_views.xml",
    ],
}
