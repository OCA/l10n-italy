# -*- coding: utf-8 -*-
# Copyright 2019 Lorenzo Battistini
# Copyright 2019 Alessandro Camilli
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Bilancio civilistico",
    "summary": "Stampa del bilancio riclassificato secondo la IV direttiva "
               "CEE",
    "version": "12.0.1.0.1",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_financial_report",
        "l10n_it_account",
    ],
    "data": [
        "views/account_view.xml",
        "wizard/trial_balance_view.xml",
        "data/cee_groups.xml",
        "report/templates/trial_balance.xml",
    ],
    "qweb": [
    ]
}
