# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura elettronica taxes compatibility',
    'version': '8.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Emissione fatture elettroniche con uso di imposte non IVA',
    'author': 'Sergio Corato, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/8.0/'
               'l10n_it_fatturapa_out_taxes',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_fatturapa_out',
        'l10n_it_vat_registries',
        ],
    "data": [
    ],
    'installable': True,
    'autoinstall': True,
    'external_dependencies': {
        'python': ['unidecode'],
    }
}
