# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Fiscal code in invoice report",
    "summary": "Italian Fiscal Code in invoice PDF",
    "version": "10.0.1.0.0",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_fiscalcode", "account"
    ],
    "data": [
        "views/report_invoice.xml"
    ],
    'auto_install': True,
}
