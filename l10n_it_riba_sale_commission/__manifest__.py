# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - Sale commission - Ri.Ba',
    'summary': 'Modulo ponte tra provvigioni agenti e Ri.Ba',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'website': 'https://github.com/OCA/l10n-italy',
    'author': 'Nextev Srl, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_commission',
        'l10n_it_ricevute_bancarie',
    ],
    'data': [
        'views/invoice_no_commission.xml',
        'views/configuration_riba_view.xml',
    ],
}
