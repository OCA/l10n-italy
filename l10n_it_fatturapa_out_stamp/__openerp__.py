# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2019 Sergio Corato
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Italian Localization - Fattura elettronica - Integrazione bollo",
    "summary": "Modulo ponte tra emissione fatture elettroniche e imposta di "
               "bollo",
    "version": "7.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_account_stamp",
    ],
    "data": [
        'data/data.xml',
    ],
}