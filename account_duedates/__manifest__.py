#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Due dates',
    'version': '12.0.4.8.31',
    'category': 'Accounting',
    'summary': 'Enhanced due dates management',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base',
        'account_due_list',
        'account_move_plus',
        'account_payment_order',
        'account_invoice_13_more',
        'account_move_line_type',
        'date_range_plus',
        'account_payment_term_plus',
        'account_payment_method',
        'account_common_mixin',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/account_invoice_view.xml',
        'view/account_move_view.xml',
        'view/account_move_line_view.xml',
        'view/account_due_list_view.xml',
        'view/partner_view.xml',
        'view/report_invoice.xml',
        'data/update_year_cron.xml',
        'data/date_range_type.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
