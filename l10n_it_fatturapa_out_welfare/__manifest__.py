#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Cassa previdenziale",
    "summary": "Registrazione della cassa previdenziale "
    "nelle fatture elettroniche in uscita",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_fatturapa_out_wt",
        "l10n_it_payment_reason",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/invoice_it_template.xml",
        "views/welfare_fund_type_amount_views.xml",
    ],
}
