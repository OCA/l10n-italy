# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Libro giornale',
    'version': '11.0.1.0.0',
    'category': 'Localization/Italy',
    'author': 'Gianmarco Conte - Dinamiche Aziendali srl, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.dinamicheaziendali.it',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'l10n_it_account',
        'date_range'
    ],
    "data": [
        'security/ir.model.access.csv',
        'report/reports.xml',
        'wizard/print_giornale.xml',
        'views/report_account_central_journal.xml',
        'views/date_range_view.xml'
    ],
    "installable": True,
}
