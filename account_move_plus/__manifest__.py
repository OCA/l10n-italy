#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Move Plus',
    'version': '12.0.0.2.6',
    'category': 'Accounting',
    'summary': 'Account move extension',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base',
        'date_range_plus',
        'account_fiscal_year',
    ],
    'data': ['views/account_move_view.xml'],
    'installable': True,
}