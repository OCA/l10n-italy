#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Assigned Banks',
    'version': '12.0.0.2.1',
    'category': 'Generic Modules/Accounting',
    'summary': 'Assign internal banks to customer or supplier',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/partner_view.xml',
    ],
    'installable': True,
}