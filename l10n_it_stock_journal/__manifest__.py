# Copyright 2109 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Stock Journal',
    'summary': """
        Stock Journal""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Alex Comba - Agile Business Group,Odoo Community Association (OCA)',
    'website': 'https://www.agilebg.com',
    'depends': [
        'stock',
        'date_range',
        'l10n_it_ddt',
    ],
    'data': [
        'wizards/stock_journal_wizard.xml',
        'report/stock_journal_report.xml'
    ],
    'installable': True,
}
