#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Invoice 13 more',
    'version': '12.0.3.3.15',
    'category': 'Accounting',
    'summary': 'Invoice like Odoo 13+',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': ['views/account_move_view.xml'],
    'installable': True,
}