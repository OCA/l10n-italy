# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Withholding tax',
    'version': '0.2',
    'category': 'Account',
    'description': """
    Withholding tax

""",
    'author': 'Openforce di Alessandro Camilli, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends": ['account', 'account_voucher'],
    "data": [
        'views/account.xml',
        'views/voucher.xml',
        'views/withholding_tax.xml',
        'wizard/create_wt_statement_view.xml',
        'security/ir.model.access.csv',
        'workflow.xml',
        ],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
