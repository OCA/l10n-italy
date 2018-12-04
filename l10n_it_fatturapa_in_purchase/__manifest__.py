# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    'name': 'Italian Localization - '
            'Fattura Elettronica - Integrazione acquisti',
    "summary": "Modulo ponte tra ricezione fatture elettroniche e acquisti",
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'author': 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_in_purchase',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_fatturapa_in',
        'purchase',
        ],
    "data": [
        "views/invoice_view.xml",
    ],
    "installable": True,
    'auto_install': True,
}
