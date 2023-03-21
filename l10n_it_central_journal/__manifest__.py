# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Libro giornale',
    'version': '12.0.1.1.4',
    "development_status": "Beta",
    'category': 'Localization/Italy',
    'author': 'Gianmarco Conte - Dinamiche Aziendali srl, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/12.0/'
               'l10n_it_central_journal',
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
