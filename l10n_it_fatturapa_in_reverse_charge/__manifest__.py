# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera (Level Prime Srl)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    'name': 'Italian Localization - '
            'Fattura elettronica - Integrazione Reverse Charge',
    "summary": "Modulo ponte tra ricezione fatture elettroniche"
               " e reverse charge",
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'author': 'Level Prime Srl, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_in_reverse_charge',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_fatturapa_in',
        'l10n_it_reverse_charge',
        ],
    "data": [],
    "installable": True,
    'auto_install': True,
}
