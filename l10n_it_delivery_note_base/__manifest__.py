# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
{
    "name": "ITA - Documento di trasporto - Base",
    "summary": "Crea e gestisce tabelle principali per gestire i DDT",
    "author": "Marco Calcagni, Gianmarco Conte, Link IT Europe Srl, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "maintainers": ["As400it", "Byloth"],
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/delivery_note_data.xml",
        "security/ir_module_category.xml",
        "security/ir_rule.xml",
        "security/res_groups.xml",
        "security/res_users.xml",
        "views/stock_delivery_note_type.xml",
        "views/stock_picking_goods_appearance.xml",
        "views/stock_picking_transport_condition.xml",
        "views/stock_picking_transport_method.xml",
        "views/stock_picking_transport_reason.xml",
    ],
}
