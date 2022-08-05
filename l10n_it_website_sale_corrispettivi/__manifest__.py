# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - E-commerce - Ricevute',
    'summary': 'Aggiunge la ricevuta come opzione per l\'utente e-commerce',
    'category': 'e-commerce',
    'author': 'Agile Business Group,'
              'Odoo Community Association (OCA)',
    'version': '12.0.1.0.1',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_website_sale_corrispettivi',
    'depends': [
        'website_sale',
        'l10n_it_corrispettivi_sale',
        'l10n_it_website_sale_fatturapa'
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
