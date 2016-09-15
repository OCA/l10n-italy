# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Fiscal year closing",
    "summary": "Generic fiscal year closing wizard",
    "version": "9.0.1.0.0",
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
        "views/account_fiscalyear_closing_view.xml",
        "views/account_fiscalyear_closing_mapping_view.xml",
        "views/account_fiscalyear_closing_type_view.xml",
        "views/account_fiscalyear_closing_config_view.xml",
        "views/account_move_view.xml",
        "views/account_move_line_view.xml",
    ],
}
