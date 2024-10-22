# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Libro giornale - Reportlab',
    'version': '12.0.1.0.0',
    "development_status": "Beta",
    'category': 'Localization/Italy',
    'author': 'Gianmarco Conte - Dinamiche Aziendali srl, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'maintainers': ['MarcoCalcagni', 'Borruso'],
    "depends": [
        'account',
        'date_range'
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/print_giornale.xml',
        'views/account_journal_view.xml',
        'views/date_range_view.xml'
    ],
    "installable": True,
}
