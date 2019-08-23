# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2019 Sergio Corato (info@efatto.it)
# Copyright 2019 Glauco Prina (gprina@linkgroup.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Dichiarazione Intento',
    'summary': """
        Gestione dichiarazione di intento""",
    'version': '11.0.0.1.0',
    'license': 'AGPL-3',
    'author': 'Francesco Apruzzese, Odoo Community Association (OCA), '
              'Sergio Corato, Glauco Prina',
    'website': 'https://github.com/OCA/l10n-italy/tree/'
               '11.0/l10n_it_dichiarazione_intento',
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
