# coding=utf-8
# Leonardo Donelli - Creativi Quadrati
# © 2016 Alessio Gerace - Agile Business Group
# © 2018-2019 Lorenzo Battistini
# © 2019 Roberto Fichera - Level Prime Srl
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Driver for ePOS-Print XML compatible fiscal printers',
    'version': '10.0.1.0.0',
    'category': 'POS, Fiscal, Hardware, Driver',
    'summary': 'ePOS-Print XML Fiscal Printer Driver',
    'author': (
        'Agile Business Group, '
        'Leonardo Donelli @ Creativi Quadrati, TAKOBI, '
        'Level Prime Srl'
    ),
    'website': 'https://takobi.online',
    'depends': [
        'point_of_sale',
        'pos_order_mgmt',
    ],
    'data': [
        'views/account_statement_view.xml',
        'views/point_of_sale.xml',
        'views/assets.xml',
    ],
    'js': [
        'static/src/js/models.js',
        'static/src/js/fp90iii.js',
        'static/lib/fiscalprint/fiscalprint.js'
    ],
    'qweb': [
        'static/src/xml/pos.xml'
    ],
    'installable': True,
    'auto_install': False,
}
