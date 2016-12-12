# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - FatturaPA - Emission',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices emission',
    'author': 'Davide Corio, Agile Business Group, Innoviu',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa',
        'l10n_it_split_payment',
        ],
    "data": [
        'wizard/wizard_export_fatturapa_view.xml',
        'views/attachment_view.xml',
        'views/account_view.xml',
        'security/ir.model.access.csv',
    ],
    "test": [],
    'installable': True,
    'external_dependencies': {
        'python': ['unidecode'],
    }
}
