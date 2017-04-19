# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "E-commerce: corrispettivi",
    "summary": "Issue invoices or receipts for e-commerce orders",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "http://www.agilebg.com",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_corrispettivi",
        "website_sale",
    ],
    "data": [
        "views/checkout.xml",
        "views/sale_order_view.xml",
    ],
}
