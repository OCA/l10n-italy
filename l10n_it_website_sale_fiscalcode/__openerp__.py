# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Sale FiscalCode',
    'category': 'e-commerce',
    "author": 'Agile Business Group, '
              'Odoo Community Association (OCA)',
    "license": "AGPL-3",
    'version': '8.0.1.0.0',
    'website': 'http://www.agilebg.com',
    'depends': [
        'website_sale_partner_type',
        'l10n_it_fiscalcode',
        'l10n_it_sale_associations'
    ],
    'data': [
        'views/templates.xml',
        'views/assets.xml',
    ],
    'installable': True,
}
