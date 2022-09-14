# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Imposta di bollo - Vendite',
    'summary': "Modulo ponte tra imposta di bollo e vendite",
    'version': '12.0.1.0.1',
    'category': 'Localization/Italy',
    'license': 'AGPL-3',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'maintainers': ['tafaRU'],
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_account_stamp_sale',
    'depends': [
        'l10n_it_account_stamp',
        'sale',
    ],
    'auto_install': True,
    'installable': True,
}
