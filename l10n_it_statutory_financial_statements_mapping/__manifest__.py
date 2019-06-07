# -*- coding: utf-8 -*-
# Copyright 2019 Francesco Apruzzese
# Copyright 2019 Ilaria Franchini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Statutory_financial statements mapping",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Odoo Community Association (OCA)",
    "maintainers": ["ilaria-franchini","OpenCode"],
    "license": "LGPL-3",
    "post_init_hook": "cee_group_mapping_init",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_statutory_financial_statements",
        "l10n_it",
    ],
}
