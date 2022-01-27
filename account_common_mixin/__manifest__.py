#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Common Mixin',
    'version': '12.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Common account fields',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_invoice_13_more',
        'assigned_bank',
        'l10n_it_fiscal_payment_term',
    ],
    'data': [
        'views/account_move_view.xml',
        'views/account_invoice_view.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
