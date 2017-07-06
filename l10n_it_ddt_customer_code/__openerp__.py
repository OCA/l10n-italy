# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Product Customer code for DDT",
    "version": "8.0.1.0.0",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "website": "http://www.agilebg.com",
    "license": 'AGPL-3',
    "category": "Stock",
    "depends": [
        'product_customer_code_picking',
        'l10n_it_ddt',
    ],
    "data": [
        'views/report_ddt.xml',
    ],
    "installable": True,
    "images": [
        'images/ddt.png',
    ],
}
