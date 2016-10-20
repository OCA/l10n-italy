# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Withholding Tax',
    'version': '8.0.3.0.0',
    'category': 'Account',
    'author': 'Openforce, Odoo Italia Network, '
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    "depends": ['account'],
    "data": [
        'views/account.xml',
        'views/withholding_tax.xml',
        'security/ir.model.access.csv',
        'workflow.xml',
    ],
    "active": False,
    "installable": True
}
