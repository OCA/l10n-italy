# -*- coding: utf-8 -*-
# Copyright 2017 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'DDT Shipping Costs',
    'version': '8.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'DDT Spese di trasporto',
    'author': 'Andrea Cometa, Apulia Software,'
              'Odoo Community Association (OCA),',
    'website': 'http://www.odoo-italia.org/',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_ddt',
        'stock_picking_package_preparation_value',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/partner_view.xml',
        ],
    'installable': True,
}
