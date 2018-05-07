# -*- coding: utf-8 -*-
# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Withholding Tax',
    'version': '10.0.1.2.2',
    'category': 'Account',
    'author': 'Openforce, Odoo Italia Network, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.odoo-italia.net/',
    'license': 'AGPL-3',
    "depends": ['account'],
    "data": [
        'views/account.xml',
        'views/withholding_tax.xml',
        'security/ir.model.access.csv',
        'workflow.xml',
        'security/security.xml',
    ],
    "installable": True
}
