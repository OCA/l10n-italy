# -*- coding: utf-8 -*-
# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2018  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Split Payment',
    'version': '10.0.1.1.0',
    'category': 'Localization/Italy',
    'summary': 'Split Payment',
    'author': 'Abstract, Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'views/account_view.xml',
        'views/config_view.xml',
    ],
    'installable': True,
}
