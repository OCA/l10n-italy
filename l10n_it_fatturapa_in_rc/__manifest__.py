# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - Fattura elettronica - integrazione fattura'
            'in acquisto e reverse charge',
    "summary": "Modulo di collegamento tra fattura in acquisto e reverse"
               " charge",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/tree/10.0/'
               'l10n_it_fatturapa_in_rc',
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "autoinstall": True,
    "depends": [
        "l10n_it_reverse_charge",
        "l10n_it_fatturapa_in",
    ],
    "data": [
    ],
}
