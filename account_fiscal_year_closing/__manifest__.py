# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2016-2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fiscal year closing",
    "summary": "Generic fiscal year closing wizard",
    "version": "10.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://www.tecnativa.org/",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_reversal",
    ],
    "data": [
        "security/account_fiscalyear_closing_security.xml",
        "security/ir.model.access.csv",
        "views/account_fiscalyear_closing_views.xml",
        "views/account_fiscalyear_closing_template_views.xml",
        "views/account_move_views.xml",
        "wizards/account_fiscal_year_closing_unbalanced_move_views.xml",
    ],
}
