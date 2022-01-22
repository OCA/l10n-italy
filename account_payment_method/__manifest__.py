#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Payment Method',
    'version': '12.0.0.2.8',
    'category': 'Generic Modules/Accounting',
    'summary': 'Extended payment method',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'account_payment_mode',
    ],
    'data': [
        'views/payment_method_view.xml',
        'data/payment_method.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
