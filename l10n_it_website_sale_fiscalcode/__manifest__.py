# -*- coding: utf-8 -*-
# Copyright 2017 Nicola Malcontenti - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/Lgpl).

{
    'name': 'Website Sale FiscalCode',
    'category': 'e-commerce',
    'author': "Agile Business Group,"
              "Odoo Community Association (OCA)",
    'version': '10.0.1.0.1',
    'license': 'LGPL-3',
    'website': 'http://www.agilebg.com',
    'depends': [
        'website_sale',
        'l10n_it_fiscalcode'
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
