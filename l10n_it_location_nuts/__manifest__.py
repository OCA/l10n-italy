# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'NUTS Regions for Italy',
    'summary': 'NUTS specific options for Italy',
    'version': '10.0.1.0.0',
    'category': 'Localisation/Europe',
    'website': 'https://www.agilebg.com',
    'author': 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base_location_nuts',
    ],
    'post_init_hook': 'post_init_hook',
}
