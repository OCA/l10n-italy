# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Sergio Corato
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura elettronica - Emissione',
    'version': '10.0.2.0.0',
    'category': 'Localization/Italy',
    'summary': 'Emissione fatture elettroniche',
    'author': 'Davide Corio, Agile Business Group, Innoviu,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy'
               'l10n_it_fatturapa_out',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_fatturapa',
        'l10n_it_split_payment',
        ],
    "data": [
        'wizard/wizard_export_fatturapa_view.xml',
        'views/attachment_view.xml',
        'views/account_view.xml',
        'views/partner_view.xml',
        'views/company_view.xml',
        'security/ir.model.access.csv',
        'data/l10n_it_fatturapa_out_data.xml',
        'security/rules.xml',
    ],
    'installable': True,
    'external_dependencies': {
        'python': [
            'unidecode',
            'pyxb',  # pyxb 1.2.6
        ],
    }
}
