# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    'name': 'Fattura Elettronica - Purchase integration',
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'author': 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
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
