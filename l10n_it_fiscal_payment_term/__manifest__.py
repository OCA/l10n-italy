# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2019 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Termini fiscali di pagamento',
    'version': '12.0.2.0.0',
    'category': 'Localization/Italy',
    'summary': 'Condizioni di pagamento delle fatture elettroniche',
    'author': 'Davide Corio, Agile Business Group, Innoviu, '
              'Odoo Italia Network, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_fiscal_payment_term',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/fatturapa_data.xml',
        'views/account_view.xml',
    ],
    'installable': True
}
