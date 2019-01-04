# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################
{
    'name': 'Italian Localization - Fiscal payment mode',
    'version': '8.0.0.1.0',
    'category': 'Localisation/Italy',
    'author': "Elven Studio S.N.C.",
    'summary': 'Electronic invoices payment mode',
    'website': 'http://www.elvenstudio.it',
    'license': 'LGPL-3',

    'depends': [
        'l10n_it_fiscal_payment_term',
        'account_payment',
    ],

    'data': [
        'views/payment_mode_view.xml',
    ],

    'installable': True
}
