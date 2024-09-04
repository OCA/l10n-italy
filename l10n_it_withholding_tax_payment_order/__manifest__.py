# Copyright 2024 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Ritenute d'acconto - Ordini di pagamento",
    "summary": "Integrazione Ritenute d'acconto e Ordini di pagamento",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Innovyou, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_withholding_tax",
        "account_payment_order",
    ],
    "data": [],
}
