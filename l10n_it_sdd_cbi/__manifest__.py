# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - SEPA Direct Debit",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Create SEPA files for CBI SDD Italy",
    "author": "Dinamiche Aziendali srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account_payment_order",
        "account_banking_pain_base",
        "account_banking_mandate",
        "account_banking_sepa_direct_debit",
        "l10n_it_abicab",
    ],
    "data": [
        "data/account_payment_method.xml",
        "views/account_payment_order_view.xml",
        "views/res_config_settings_view.xml",
    ],
    "installable": True,
}
