# -*- coding: utf-8 -*-
# Copyright 2017 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/Agpl).

{
    'name': 'Website Sale FiscalCode',
    'category': 'e-commerce',
    'author': "Agile Business Group,"
              "Odoo Community Association (OCA)",
    'version': '10.0.1.0.2',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/l10n-italy',
    'depends': [
        'website_sale',
        'l10n_it_fiscalcode'
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
