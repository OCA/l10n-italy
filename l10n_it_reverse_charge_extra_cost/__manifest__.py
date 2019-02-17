# -*- coding: utf-8 -*-
# Copyright 2019 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Reverse Charge IVA Extra cost on self invoice',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Reverse Charge for Italy cost on self invoice',
    'author': 'Dinamiche Aziendali srl',
    'license': 'LGPL-3',
    'website': 'https://www.dinamicheaziendali.it',
    'depends': [
        'account_accountant',
        'account_cancel',
        'l10n_it_reverse_charge',
    ],
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
