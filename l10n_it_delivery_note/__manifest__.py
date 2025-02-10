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
    "version": "18.0.1.0.1",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "maintainers": ["MarcoCalcagni", "aleuffre", "renda-dev"],
    "depends": [
        "delivery_carrier_partner",
        "mail",
        "sale",
        "sale_stock",
        # "stock_account",
        "stock_delivery",
        "portal",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_module_category.xml",
        "security/ir_rule.xml",
        "security/res_groups.xml",
        "security/res_users.xml",
        "data/delivery_note_data.xml",
        "report/delivery_data.xml",
        "report/report_delivery_note.xml",
        "views/account_move.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/stock_delivery_note_type.xml",
        "views/stock_picking_goods_appearance.xml",
        "views/stock_picking_transport_condition.xml",
        "views/stock_picking_transport_method.xml",
        "views/stock_picking_transport_reason.xml",
        "views/stock_delivery_note.xml",
        "views/stock_picking.xml",
        "views/portal_templates.xml",
        "views/portal_my_delivery_notes.xml",
        "wizard/delivery_note_confirm.xml",
        "wizard/delivery_note_create.xml",
        "wizard/delivery_note_invoice.xml",
        "wizard/delivery_note_select.xml",
        "wizard/delivery_note_template.xml",
        "wizard/sale_advance_payment_inv.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
        "demo/delivery_carrier_demo.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "l10n_it_delivery_note/static/src/scss/stock_delivery_note.scss",
        ],
    },
    "post_init_hook": "post_init_hook",
}
