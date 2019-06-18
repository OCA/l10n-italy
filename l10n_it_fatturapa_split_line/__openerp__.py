# -*- coding: utf-8 -*-
# Copyright 2019 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - Split invoice line > 1000 chars',
    "summary": "Le righe fattura non sono accettate nel canale SDI se superano"
               " i 1000 caratteri.",
    "version": "8.0.1.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Efatto.it di Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        'wizard/account_invoice_split_line.xml',
    ],
}
