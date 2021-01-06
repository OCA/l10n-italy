# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Italian Localization - Fattura elettronica - Integrazione SO",
    "summary": "Modulo ponte tra emissione fatture elettroniche e dati "
               "ordine di vendita",
    "version": "8.0.2.0.1",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Efatto.it, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "sale",
    ],
    "data": [
        "views/partner_view.xml",
        "views/account_view.xml",
        "views/company_view.xml",
    ],
}
