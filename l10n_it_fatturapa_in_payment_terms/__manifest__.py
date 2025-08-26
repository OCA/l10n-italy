# Copyright 2025 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Payment Terms from XML',
    'version': '12.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Retrieve payment terms from FatturaPA XML',
    'author': 'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_fatturapa_in',
        'account',
    ],
    'data': [
        'views/account_payment_term_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}