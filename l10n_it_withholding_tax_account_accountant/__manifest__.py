{
    "name": "ITA - Ritenute d'acconto account_accountant",
    "summary": """
        Integrazione ritenute d'acconto tra l10n_it_withholding_tax e
        account_accountant.
    """,
    "author": "Innovyou, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "category": "Hidden",
    "version": "16.0.1.0.0",
    "auto_install": True,
    "license": "AGPL-3",
    "depends": ["base", "l10n_it_withholding_tax", "account_accountant"],
    "data": [
        "views/bank_rec_widget_views.xml",
    ],
}
