# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>,
# Copyright 2019 Alessandro Camilli <alessandrocamilli@openforce.it>,
# Link IT <info@linkgroup.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Dichiarazione di intento',
    'summary': 'Gestione dichiarazioni di intento',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Francesco Apruzzese, Odoo Community Association (OCA), '
              'Sergio Corato, Glauco Prina, Lara Baggio',
    'website': 'https://github.com/OCA/l10n-italy/tree/'
               '10.0/l10n_it_dichiarazione_intento',
    'depends': [
        'account',
        'sale',
        ],
    'data': [
        'wizard/manually_declarations_view.xml',
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
