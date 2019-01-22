# -*- coding: utf-8 -*-
# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Localization - Fattura elettronica - '
            'Integrazione sconto triplo',
    "summary": "Modulo ponte tra emissione "
               "fatture elettroniche e sconto triplo",
    "version": "8.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/8.0/'
               'l10n_it_fatturapa_out_triple_discount',
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "account_invoice_triple_discount",
    ]
}
