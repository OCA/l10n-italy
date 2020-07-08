# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# noinspection PyStatementEffect
{
    'name': "ITA - Documento di Trasporto Base",
    'summary': "Crea, gestisci e fattura i DdT partendo dalle Consegne",

    'author': "Marco Calcagni, Gianmarco Conte, Link IT Europe Srl",
    'website': 'https://github.com/OCA/l10n-italy/tree/12.0/'
               'l10n_it_delivery_note_base',
    'version': '12.0.1.0.0',
    'category': "Localization",

    'data': [
        'data/delivery_note_data.xml',

        'security/ir_rule.xml',

        'views/stock_delivery_note_type.xml',
        'views/stock_picking_goods_appearance.xml',
        'views/stock_picking_transport_condition.xml',
        'views/stock_picking_transport_method.xml',
        'views/stock_picking_transport_reason.xml'
    ]
}
