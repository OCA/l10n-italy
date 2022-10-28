# -*- coding: utf-8 -*-
# Copyright 2015 Nicola Malcontenti - Agile Business Group
# Copyright 2016 Andrea Cometa - Apulia Software
# Copyright 2016-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Account invoice report grouped by DDT",
    'version': '10.0.0.3.2',
    'category': 'Localization/Italy',
    'author': 'Agile Business Group, Apulia Software, Openforce,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': [
        'account', 'l10n_it_ddt',
    ],
    "data": [
        'views/invoice_ddt.xml',
        'views/partner.xml',
    ],
    "installable": True
}
