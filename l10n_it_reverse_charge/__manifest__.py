# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Inversione contabile',
    'version': '12.0.1.3.0',
    'category': 'Localization/Italy',
    'summary': 'Inversione contabile',
    'author': 'Odoo Italia Network, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_reverse_charge',
    'depends': [
        'account',
        'account_cancel',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/rc_type.xml',
        'views/account_invoice_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_rc_type_view.xml',
        'security/reverse_charge_security.xml',
    ],
    'installable': True,
}
