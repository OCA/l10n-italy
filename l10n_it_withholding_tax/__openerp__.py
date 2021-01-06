# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Withholding Tax',
    'version': '8.0.4.0.1',
    'category': 'Account',
    'author': 'Openforce di Alessandro Camilli, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['account', 'account_voucher', 'product'],
    "data": [
        'views/account.xml',
        'views/voucher.xml',
        'views/withholding_tax.xml',
        'views/product.xml',
        'wizard/create_wt_statement_view.xml',
        'security/ir.model.access.csv',
        'workflow.xml',
    ],
    "installable": True
}
