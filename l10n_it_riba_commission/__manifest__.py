# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Ricevute bancarie & commissioni",
    "summary": "Ricevute bancarie & commissioni",
    "version": "10.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/l10n-italy/tree/10.0/"
               "l10n_it_riba_commission",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_ricevute_bancarie",
        "sale_commission"
    ],
    "auto_install": True,
    "data": ["views/sale_commission.xml"]
}
