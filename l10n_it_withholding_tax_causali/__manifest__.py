# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Causali pagamento per ritenute d'acconto",
    "version": "12.0.2.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_withholding_tax_causali",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_withholding_tax",
        "l10n_it_causali_pagamento",
    ],
    "data": [
        "views/withholding_tax.xml",
    ],
    'auto_install': True,
}
