# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Italian Localization - Email PEC',
    'version': '12.0.1.0.1',
    'category': 'Localization/Italy',
    'summary': 'Aggiunge il campo email PEC al partner',
    'author': "Odoo Italia Network,Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_pec',
    'license': 'AGPL-3',
    'depends': ['mail'],
    'data': [
        'views/partner_view.xml',
    ],
    'installable': True,
}
