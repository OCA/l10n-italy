# Copyright 2025
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Reverse Charge - Fixed Discount Integration',
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Integrates fixed discount with reverse charge self-invoices',
    'author': 'TAKOBI, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    'depends': [
        'l10n_it_reverse_charge',
        'account_invoice_fixed_discount',
    ],
    'data': [],
    'installable': True,
    'auto_install': True,
}
