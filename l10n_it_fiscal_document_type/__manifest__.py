# Copyright 2017 Alessandro Camilli
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - '
            'Tipi di documento fiscali per dichiarativi',
    'version': '11.0.1.0.0',
    'category': 'Localisation/Italy',
    'author': "Link It srl, Odoo Community Association (OCA)",
    'website': 'https://www.odoo-italia.net/',
    'license': 'LGPL-3',
    'depends': ['l10n_it_account'],
    'data': [
        'views/fiscal_document_type_view.xml',
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/account_view.xml',
        'data/fiscal.document.type.csv',
        "security/ir.model.access.csv"
    ],

    'installable': True
}
