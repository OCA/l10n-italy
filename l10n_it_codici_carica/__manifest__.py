# -*- coding: utf-8 -*-
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
# Copyright 2017 Alessandro Camilli - Openforce
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
=======
# © 2017 Alessandro Camilli - Openforce
#
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
>>>>>>> 0590845b855585f5431727c60908bce98ac81350
=======
# © 2017 Alessandro Camilli - Openforce
#
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
>>>>>>> 0590845... Tabelle dei codici carica da usale nelle dichiarazioni fiscali
=======
# Copyright 2017 Alessandro Camilli - Openforce
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
>>>>>>> 8c63b3189e4a62762a6e72087b2dcfc60e1b2df1


{
    'name': 'Codici Carica',
    'summary':
        'Aggiunge la tabella dei codici carica da usare nei dichiarativi'
        ' fiscali italiani',
    'version': '10.0.1.0.0',
    'category': 'Account',
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    'author': "Openforce di Camilli Alessandro"
        "Odoo Community Association (OCA)",
    'website': 'http://odoo-italia.net',
=======
    'author': "Openforce di Camilli Alessandro",
    'website': 'https://odoo-community.org/',
>>>>>>> 0590845b855585f5431727c60908bce98ac81350
=======
    'author': "Openforce di Camilli Alessandro",
    'website': 'https://odoo-community.org/',
>>>>>>> 0590845... Tabelle dei codici carica da usale nelle dichiarazioni fiscali
=======
    'author': "Openforce di Camilli Alessandro"
        "Odoo Community Association (OCA)",
    'website': 'http://odoo-italia.net',
>>>>>>> 8c63b3189e4a62762a6e72087b2dcfc60e1b2df1
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
