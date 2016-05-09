# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Withholding Tax Payment',
    'version': '8.0.2.0.0',
    'category': 'Account',
    'author': 'Openforce di Alessandro Camilli, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['l10n_it_withholding_tax'],
    "data": [
        'views/withholding_tax.xml',
        'workflow.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/create_move_payment_view.xml',
        ],
    "active": False,
    "installable": True
}
