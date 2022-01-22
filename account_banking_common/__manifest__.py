#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
{
    'name': 'Account Banking Common',
    'version': '12.0.3.7.25',
    'category': 'Accounting',
    'summary': 'Common stuff for payment modules',
    'author': 'powERP enterprise network and other partners',
    'website': 'https://www.powerp.it',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_due_list',
        'account_duedates',
        'account_payment_order',
        'account_payment_method',
        'l10n_it_iban_in_stampa',
    ],
    'data': [
        'views/res_partner_bank_view.xml',
        'views/action_insoluto.xml',
        'wizard/wizard_insoluto.xml',
        'wizard/wizard_payment_order_confirm.xml',
        'wizard/wizard_payment_order_credit.xml',
        'wizard/wizard_account_payment_order_generate.xml',
        'wizard/wizard_account_payment_order_add_move_lines.xml',
        'wizard/wizard_set_payment_method.xml',
        'views/action_payment_confirm.xml',
        'views/account_payment_order.xml',
        'views/action_order_generate.xml',
        'views/action_order_add_move_lines.xml',
        'views/action_duedates_update.xml',
        'views/account_bank_journal_form.xml',
        'views/account_invoice_view.xml',
    ],
    'maintainer': 'powERP enterprise network',
    'installable': True,
}
