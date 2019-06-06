# -*- coding: utf-8 -*-
# Copyright 2019 Lorenzo Battistini
# Copyright 2019 Alessandro Camilli
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "ITA - Bilancio civilistico",
    "summary": "Stampa del bilancio riclassificato secondo la IV direttiva "
               "CEE",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Odoo Community Association (OCA)",
    "maintainers": ["eLBati", "OpenCode"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account_financial_report_qweb",
        "l10n_it_account",
        "account_group",
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
