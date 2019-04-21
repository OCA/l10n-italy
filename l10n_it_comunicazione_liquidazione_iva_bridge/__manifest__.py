# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
# © 2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Comunicazione liquidazione IVA Bridge',
    'summary': 'Bridge per importare i dati della liquidazione iva nella'
    'comunicazione liquidazione IVA',
    'version': '10.0.0.1.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'https://www.odoo-italia.net',
    'license': 'LGPL-3',
    'depends': [
        'account_vat_period_end_statement',
        'l10n_it_comunicazione_liquidazione_iva'
    ],
    'data': [
        'views/comunicazione_liquidazione.xml',
    ],
    'installable': True,
}
