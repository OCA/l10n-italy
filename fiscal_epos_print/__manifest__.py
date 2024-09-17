# Leonardo Donelli - Creativi Quadrati
# © 2016 Alessio Gerace - Agile Business Group
# © 2018-2019 Lorenzo Battistini
# © 2019-2020 Roberto Fichera - Level Prime Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ITA - Driver per stampanti fiscali compatibili ePOS-Print XML',
    'version': '12.0.1.2.1',
    'category': 'Point Of Sale',
    'summary': 'ePOS-Print XML Fiscal Printer Driver - Stampanti Epson compatibili: '
               'FP81II, FP90III',
    'author': (
        'Odoo Community Association (OCA), Agile Business Group, '
        'Leonardo Donelli, TAKOBI, Level Prime Srl'
    ),
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/l10n-italy',
    'depends': ['point_of_sale', 'pos_order_mgmt'],
    'data': [
        'views/account.xml',
        'views/point_of_sale.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
    'auto_install': False,
}
