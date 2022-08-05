# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2019 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'ITA - Regioni NUTS',
    'summary': 'Opzioni NUTS specifiche per l\'Italia',
    'version': '12.0.1.0.2',
    'category': 'Localisation/Europe',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_location_nuts',
    'author': 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base_location_nuts',
    ],
    'post_init_hook': 'post_init_hook',
}
