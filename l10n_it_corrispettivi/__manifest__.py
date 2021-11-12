# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Simone Rubino - Agile Business Group
# Copyright 2019 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2020 Giovanni Serra - GSLab.it
# Copyright 2021 Kevin Poli - AIR s.r.l.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Italian Localization - Ricevute',
    'version': '14.0.1.0.0',
    'category': 'Accounting & Finance',
    'author': 'Odoo Italian Community,AIR s.r.l, Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/airsrl/l10n-italy/tree/14.0/'
               'l10n_it_corrispettivi',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'data/account_journal_data.xml',
        'views/account_report.xml',
        'views/account_view.xml'
    ],
    'installable': True
}
