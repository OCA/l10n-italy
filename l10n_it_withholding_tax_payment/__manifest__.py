# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# Copyright 2019 Matteo Bilotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "ITA - Ritenuta d'acconto - Pagamenti",
    'summary': "Gestisce le ritenute sulle fatture e sui pagamenti",
    'version': '12.0.1.0.1',
    'development_status': "Beta",
    'category': "Invoicing & Payments",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_withholding_tax_payment',
    'author': "Openforce, "
              "Odoo Italia Network, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account',
        'l10n_it_withholding_tax'
    ],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/withholding_tax.xml',
        'wizard/create_move_payment_view.xml',
    ]
}
