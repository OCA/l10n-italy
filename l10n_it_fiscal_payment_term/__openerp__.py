# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Andrea Cometa - Apulia Software
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fiscal payment term',
    'version': '0.0.1',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices payment',
    'author': 'Davide Corio, Agile Business Group, Innoviu, '
              'Apulia Software, '
              'Odoo Italia Network, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org',
    'license': 'Other OSI approved licence',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/fatturapa_data.xml',
        'views/account_view.xml',
    ],
    'installable': True,
    'pre_init_hook': 'pre_init_hook',
}
