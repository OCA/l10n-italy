# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura Elettronica - Integrazione DDT',
    "summary": "Modulo ponte tra emissione fatture elettroniche e DDT",
    "version": "10.0.1.0.2",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_out_ddt',
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
