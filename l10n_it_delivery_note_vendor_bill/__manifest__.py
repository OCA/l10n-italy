# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Delivery Note - Vendor Bill",
    "summary": "Autofill vendor bill from a delivery note",
    "author": "PyTech SRL, Ooops, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "maintainers": ["aleuffre", "renda-dev", "PicchiSeba"],
    "category": "Localization/Italy",
    "depends": [
        "html_text",
        "l10n_it_delivery_note",
        "purchase_stock",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
}
