# -*- coding: utf-8 -*-
# Leonardo Donelli - Creativi Quadrati
# © 2016 Alessio Gerace - Agile Business Group
# © 2018-2019 Lorenzo Battistini
# © 2019-2020 Roberto Fichera - Level Prime Srl
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'ITA - Driver per stampanti fiscali compatibili ePOS-Print XML',
    'version': '10.0.1.0.0',
    'category': 'Point Of Sale',
    'summary': 'ePOS-Print XML Fiscal Printer Driver - Stampanti Epson compatibili'
               'FP81II, FP90III',
    'author': (
        'Agile Business Group, '
        'Leonardo Donelli @ Creativi Quadrati, TAKOBI, '
        'Roberto Fichera @ Level Prime Srl'
    ),
    'website': 'https://takobi.online',
    'depends': [
        'point_of_sale',
        'pos_order_mgmt',
    ],
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
