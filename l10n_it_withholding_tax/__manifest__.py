# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Withholding Tax',
    'version': '12.0.1.0.0',
    'category': 'Account',
    'author': 'Openforce, Odoo Italia Network, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    "depends": ['account'],
    "data": [
        'views/account.xml',
        'views/withholding_tax.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'qweb': [
        "static/src/xml/account_payment.xml",
    ],
    "installable": True
}
