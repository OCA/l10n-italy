# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2022 Marco Colombo - <marco.colombo@phi.technology>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Causali pagamento per ritenute d'acconto",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_withholding_tax",
        "l10n_it_payment_reason",
    ],
    "data": [
        "views/withholding_tax.xml",
    ],
    "auto_install": True,
}
