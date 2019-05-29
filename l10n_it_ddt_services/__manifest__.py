# -*- coding: utf-8 -*-
#
#    Copyright (C) 2019 Giacomo Grasso
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#

{
    'name': 'DDT services',
    'version': '10.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Fatturazione Servizi dal Documento di Trasporto',
    'author': 'Giacomo Grasso, Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_ddt',
        'sale',
    ],
    'data': [
        'views/models.xml'
    ],
    'installable': True,
}
