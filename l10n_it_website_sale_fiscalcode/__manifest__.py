# Copyright 2017 Nicola Malcontenti - Agile Business Group
# Copyright 2019 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Website Sale FiscalCode',
    'category': 'e-commerce',
    'author': "Agile Business Group,"
              "Odoo Community Association (OCA)",
    'version': '12.0.1.1.3',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_website_sale_fiscalcode',
    'depends': [
        'website_sale',
        'l10n_it_fiscalcode'
    ],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
