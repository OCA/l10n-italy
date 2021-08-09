# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Reverse Charge IVA',
    'version': '10.0.1.2.3',
    'category': 'Localization/Italy',
    'summary': 'Reverse Charge for Italy',
    'author': 'Odoo Italia Network,Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'website': 'https://www.odoo-italia.net',
    'depends': [
        'account_accountant',
        'account_cancel',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/rc_type.xml',
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_rc_type_view.xml',
    ],
    'installable': True,
}
