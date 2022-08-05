# © 2017 Alessandro Camilli - Openforce
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)
#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Codici carica',
    'version': '12.0.1.0.2',
    'category': 'Localization/Italy',
    'summary':
        'Aggiunge la tabella dei codici carica da usare nelle dichiarazioni'
        ' fiscali italiane',
    'author': "Openforce di Camilli Alessandro,"
              "Odoo Community Association (OCA)",
    'website':  'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_codici_carica',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/codici_carica_data.xml',
        'views/codice_carica_view.xml',
    ],
    'installable': True,
}
