# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright 2018 Ermanno Gnan (ermannognan@gmail.com)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Tax Stamp',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Tax stamp automatic management',
    'author': 'Ermanno Gnan, Sergio Corato, Enrico Ganzaroli, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'account',
    ],
    'data': [
        'data/data.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
        'views/company_view.xml',
    ],
    'installable': True,
}
