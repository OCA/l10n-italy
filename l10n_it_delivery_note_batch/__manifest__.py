# Copyright 2020 Marco Colombo <marco.colombo@gmail.com>
# @author: Marco Colombo <marco.colombo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    "name": "ITA - Documento di trasporto - Prelievo raggruppato",
    "summary": "Crea i DDT partendo da gruppi di prelievi",
    "author": "Marco Colombo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy" "l10n_it_delivery_note_batch",
    "version": "16.0.1.1.0",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "maintainers": [
        "MarcoCalcagni",
        "TheMule71",
        "Borruso",
        "aleuffre",
        "PicchiSeba",
        "renda-dev",
    ],
    "depends": [
        "stock",
        "stock_picking_batch",
        "l10n_it_delivery_note",
    ],
    "data": [
        "views/stock_picking_batch_views.xml",
        "views/stock_picking_views.xml",
    ],
    "auto_install": True,
}
