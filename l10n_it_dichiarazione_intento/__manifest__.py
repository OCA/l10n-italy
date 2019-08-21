# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2019 Sergio Corato (info@efatto.it)
# Copyright 2019 Glauco Prina (gprina@linkgroup.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Dichiarazione Intento',
    'summary': """
        Manage italian dichiarazione di intento""",
    'version': '12.0.0.1.0',
    'license': 'AGPL-3',
    'author': 'Francesco Apruzzese, Odoo Community Association (OCA), '
              'Sergio Corato, Glauco Prina',
    'website': 'https://odoo-community.org/',
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'views/account_view.xml',
        'views/dichiarazione_intento_view.xml',
        'views/company_view.xml',
        'views/account_invoice_view.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
