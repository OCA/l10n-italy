# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# noinspection PyStatementEffect
{
    "name": "ITA - Documento di trasporto",
    "summary": "Crea, gestisce e fattura i DDT partendo dalle consegne",
    "author": "Marco Calcagni, Gianmarco Conte, Link IT Europe Srl, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "version": "14.0.1.0.1",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "maintainers": ["As400it", "Byloth"],
    "depends": [
        "delivery",
        "l10n_it_delivery_note_base",
        "mail",
        "sale_stock",
        "stock_account",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "security/res_groups.xml",
        "security/res_users.xml",
        "report/report_delivery_note.xml",
        "views/account_move.xml",
        "views/assets.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/stock_delivery_note.xml",
        "views/stock_picking.xml",
        "wizard/delivery_note_create.xml",
        "wizard/delivery_note_select.xml",
        "wizard/delivery_note_template.xml",
        "wizard/sale_advance_payment_inv.xml",
    ],
}
