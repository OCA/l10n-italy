# -*- coding: utf-8 -*-
# Copyright 2019 Giacomo Grasso, Gabriele Baldessari
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "ITA - Aggiornamento valute Banca d'Italia",
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': 'Modulo per aggiornare i tassi di cambio automaticamente '
               'con i dati della Banca d\'Italia.',
    'author': 'Giacomo Grasso, Gabriele Baldessari,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/'
               '10.0/l10n_it_currency_update',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'currency_rate_update'],
    'data': [],
    'installable': True,
    'auto-install': False,
}
