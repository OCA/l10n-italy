# -*- coding: utf-8 -*-
# © 2021 Giuseppe Stoduto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'AltriDatiGestionali E-bill line',
    'summary':  'Imposta dei campi per inserirli nelle linee prodotti nel tag "AltriDatiGestionali"',
    'version':  '8.0.1.0.0',
    'license':  'AGPL-3',
    'author':   "Giuseppe Stoduto, "
                "Odoo Community Association (OCA)",
    'category': 'Localization/Italy',
    'depends': [
        'l10n_it_fatturapa',
        'l10n_it_fatturapa_out',
        ],
    'website':  'https://github.com/OCA/l10n-italy/tree/8.0/'
                'l10n_it_fatturapa_out_AltriDatiGestionali',
    'data': [
        'wizard/wizard_view_fields.xml',
        'views/custom_field_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
