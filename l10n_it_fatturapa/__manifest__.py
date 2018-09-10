# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura Elettronica - Base',
    'version': '10.0.2.0.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices',
    'author': 'Davide Corio, Agile Business Group, Innoviu, '
              'Odoo Italia Network, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_account',
        'l10n_it_fiscalcode',
        'document',
        'l10n_it_ipa',
        'l10n_it_rea',
        'base_iban',
        'l10n_it_account_tax_kind',
        'l10n_it_esigibilita_iva',
        'l10n_it_fiscal_payment_term',
        'l10n_it_split_payment',
        'l10n_it_fiscal_document_type',
        'partner_firstname',
        ],
    "data": [
        'data/fatturapa_data.xml',
        'data/welfare.fund.type.csv',
        'views/account_view.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'security/ir.model.access.csv',
    ],
    "demo": ['demo/account_invoice_fatturapa.xml'],
    'installable': True,
    'external_dependencies': {
        'python': [
            'pyxb',  # pyxb 1.2.5
        ],
    }
}
