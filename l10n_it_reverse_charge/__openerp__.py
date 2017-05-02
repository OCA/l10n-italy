# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Reverse Charge IVA',
    'version': '8.0.2.0.0',
    'category': 'Localization/Italy',
    'summary': 'Reverse Charge for Italy',
    'author': 'Abstract, Agile Business Group,'
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.odoo-italia.net',
    'depends': [
        'account_accountant',
        'account_invoice_entry_date',
        'account_cancel',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_rc_type_view.xml',

    ],
    'installable': True,
}
