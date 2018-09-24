# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "VAT registries + Split Payment",
    "summary": "Bridge module to make VAT registries work with Split Payment",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy/",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_vat_registries",
        "l10n_it_split_payment"
    ],
}
