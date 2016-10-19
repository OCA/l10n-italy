# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - FatturaPA',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices',
    'author': 'Davide Corio,Agile Business Group,Innoviu,'
              'Odoo Italia Network,Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'l10n_it_base',
        'l10n_it_fiscalcode',
        'document',
        'l10n_it_ipa',
        'l10n_it_rea',
        'base_iban',
        ],
    "data": [
        'data/fatturapa_data.xml',
        'data/welfare.fund.type.csv',
        'views/account_view.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'views/account_tax_view.xml',
        'security/ir.model.access.csv',
    ],
    "test": [],
    "demo": ['demo/account_invoice_fatturapa.xml'],
    'installable': False,
    'external_dependencies': {
        'python': ['pyxb'],
    }
}
