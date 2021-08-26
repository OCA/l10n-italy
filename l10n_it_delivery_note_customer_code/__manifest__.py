# Copyright 2021 Simone Vanin - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Product Customer code for delivery note",
    "version": "14.0.1.0.0",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "category": "Stock",
    "depends": [
        "product_supplierinfo_for_customer_picking",
        "l10n_it_delivery_note",
    ],
    "data": [
        "report/report_delivery_note.xml",
    ],
    "installable": True,
}
