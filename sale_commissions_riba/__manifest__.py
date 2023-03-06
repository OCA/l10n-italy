# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sales commissions Riba',
    'summary': 'Sales commissions extended for Riba payments',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'website': 'https://github.com/OCA/l10n-italy',
    'author': 'Nextev',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_commission',
        'l10n_it_ricevute_bancarie',
    ],
    'data': [
        'views/sale_commission_settlement_extended.xml',
        'views/invoice_no_commission.xml',
    ],
}
