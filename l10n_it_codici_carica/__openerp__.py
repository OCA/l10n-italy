# -*- coding: utf-8 -*-
# Copyright 2017 Alessandro Camilli - Openforce
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    'name': 'Codici Carica',
    'summary':
        'Aggiunge la tabella dei codici carica da usare nei dichiarativi'
        ' fiscali italiani',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro, "
        "Odoo Community Association (OCA)",
    'website': 'http://odoo-italia.net',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/codici_carica_data.xml',
        'views/codice_carica_view.xml',
    ],
    'installable': True,
}
