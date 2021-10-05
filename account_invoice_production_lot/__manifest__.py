# Copyright 2011 Domsense s.r.l. <http://www.domsense.com>
# Copyright 2013 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Invoice Production Lots",
    "version": "14.0.1.0.0+PR187",
    "author": "Agile Business Group," "Tecnativa," "Odoo Community Association (OCA)",
    "summary": "Display delivered serial numbers in invoice",
    "website": "https://github.com/OCA/account-invoice-reporting",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "depends": ["account", "stock_picking_invoice_link", "sale_management"],
    "data": ["views/account_invoice_views.xml", "report/report_invoice.xml"],
    "demo": ["demo/sale.xml"],
    "installable": True,
}
