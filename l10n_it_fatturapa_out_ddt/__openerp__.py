# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Giuseppe Stoduto
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Italian Localization - Fattura elettronica - Integrazione DDT",
    "summary": "Modulo ponte tra emissione fatture elettroniche e DDTB",
    "version": "8.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": [],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_ddt",
    ],
    "data": [
        "wizard/wizard_export_fatturapa_view.xml",
        'wizard/ddt_create_invoice.xml',
        'wizard/ddt_invoicing.xml',
        'views/account.xml',
        'views/sale.xml',
        'views/stock_picking_package_preparation.xml',
        'views/report_ddt.xml',
        'views/partner.xml',
        'data/mail_template_data.xml',
    ],
}
