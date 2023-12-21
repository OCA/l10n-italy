# Copyright 2023 Ooops404
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Delivery Note Inter Warehouse",
    "version": "14.0.1.0.0",
    "depends": [
        "l10n_it_delivery_note",
        "stock_picking_inter_warehouse",
    ],
    "author": "PyTech SRL, Ooops404, Odoo Community Association (OCA)",
    "maintainers": ["aleuffre", "renda-dev"],
    "website": "https://github.com/OCA/l10n-italy",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "data": [
        "views/stock_picking_views.xml",
        "wizards/delivery_note_select.xml",
    ],
    "installable": True,
    "application": False,
}
