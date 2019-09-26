# -*- coding: utf-8 -*-
# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Ritenuta d\'acconto - Ordine di pagamento',
    'summary': 'Modulo ponte tra ritenuta d\'acconto e ordine di pagamento',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'license': 'AGPL-3',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'maintainers': ['tafaRU'],
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_withholding_tax_payment_order',
    'depends': [
        'l10n_it_withholding_tax',
        'account_payment_order'
    ],
    'installable': True,
    'auto_install': True,
}
