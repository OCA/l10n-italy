# -*- coding: utf-8 -*-
# Author(s): Ermanno Gnan (ermannognan@gmail.com)
# Copyright © 2018 Sergio Corato (https://efatto.it)
# Copyright © 2018 Enrico Ganzaroli (enrico.gz@gmail.com)
# Copyright © 2018 Ermanno Gnan (ermannognan@gmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Tax Stamp auto add',
    'version': '7.0.0.0.1',
    'category': 'Localisation/Italy',
    'summary': 'Tax stamp auto add',
    'description': """
Tax Stamp auto add

Functionalities:

- Adds automatic tax stamp support.

""",
    'author': 'Ermanno Gnan, Sergio Corato, Enrico Ganzaroli, '
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org',
    'depends': [
        'l10n_it_account_stamp',
    ],
    'data': [
        'views/company_view.xml',
    ],
    'js': [
    ],
    'qweb': [
    ],
    'installable': True,
}
