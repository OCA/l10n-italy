# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Causali pagamento per ritenute d'acconto",
    "version": "14.0.1.0.1",
    "development_status": "Alpha",
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
    "pre_init_hook": "rename_old_italian_module",
    "auto_install": True,
}
