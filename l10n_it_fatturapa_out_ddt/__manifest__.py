# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Fattura Elettronica & DDT",
    "summary": "Bridge module",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": [],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_ddt",
    ],
    "data": [
        "wizard/wizard_export_fatturapa_view.xml"
    ],
}
