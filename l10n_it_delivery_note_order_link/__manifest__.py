# Copyright (c) 2019, Openindustry.it Sas
# @author: Andrea Piovesana <andrea.m.piovesana@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    'name': 'ITA - Documento di trasporto - Collegamento con ordine di vendita',
    'summary': 'Crea collegamento tra i DDT e ordine di vendita',
    'author': 'Openindustry.it Sas, Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_delivery_note_order_link",
    'version': '12.0.1.0.1',
    'license': 'AGPL-3',
    'maintainers': ['As400it', 'andreampiovesana'],
    'category': 'Localization',
    'depends': [
        'purchase_stock',
        'sale_stock',
        'l10n_it_delivery_note',
    ],
    'data': [
        'views/purchase_order.xml',
        'views/sale_order.xml',
    ],
}
