# -*- coding: utf-8 -*-

{
    'name': 'Italian Localisation - Tipi di documento fiscali per dichiarativi',
    'version': '1.0.0.0.0',
    'category': 'Localisation/Italy',
    'author': "Link It srl",
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': ['l10n_it_account'],
    'data': [
        'view/fiscal_document_type_view.xml',
        'view/res_partner_view.xml',
        'view/account_invoice_view.xml',
        'data/fiscal.document.type.csv',
        "security/ir.model.access.csv"
    ],

    'installable': True
}
