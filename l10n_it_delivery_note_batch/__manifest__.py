# Copyright 2020 Marco Colombo <marco.colombo@gmail.com>
# @author: Marco Colombo <marco.colombo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    'name': "ITA - Documento di Trasporto Batch Picking",
    'summary': "Crea i DdT partendo dai Gruppi di Trasferimenti",

    'author': "Marco Colombo",
    'website': "https://github.com/OCA/l10n-italy/tree/12.0/"
               "l10n_it_delivery_note_batch",

    'version': '12.0.1.0.0',
    'category': "Localization",

    'depends': [
        'stock_picking_batch',
        'l10n_it_delivery_note',
    ],

    'data': [
        'views/stock_picking_batch_views.xml',
    ],

    'auto_install': True,
}
