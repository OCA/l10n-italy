# Copyright 2018 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "ITA - Liquidazione IVA + Scissione dei pagamenti",
    'summary': "Migliora la liquidazione dell'IVA tenendo in"
               " considerazione la scissione dei pagamenti",
    'version': '12.0.1.0.2',
    'development_status': "Beta",
    'category': "Accounting & Finance",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_vat_statement_split_payment',
    'author': "Openforce Srls Unipersonale, Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'auto_install': True,
    'depends': [
        'account_vat_period_end_statement',
        'l10n_it_split_payment'
    ],
    'data': [
        'views/account_config_view.xml'
    ]
}
