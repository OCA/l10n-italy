# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "ITA - Fattura elettronica - Integrazione SO",
    "summary": "Modulo ponte tra emissione fatture elettroniche e dati "
               "ordine di vendita",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Sergio Corato, "
              "Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
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
