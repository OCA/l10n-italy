# -*- coding: utf-8 -*-
# Copyright 2019 Lorenzo Battistini @ TAKOBI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "ITA - Comunicazione liquidazione IVA e reverse charge",
    "summary": "Permette di calcolare correttamente gli importi da comunicare "
               "in presenza di reverse charge",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_vat_statement_communication",
        "l10n_it_reverse_charge",
    ],
    "data": [
    ],
    "auto_install": True,
}
