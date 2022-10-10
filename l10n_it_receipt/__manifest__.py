# Copyright 2016 Lorenzo Battistini
# Copyright 2018-2019 Simone Rubino
# Copyright 2019 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2020 Giovanni Serra - GSLab.it
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "ITA - Ricevute",
    "version": "14.0.1.0.0",
    "category": "Accounting & Finance",
    "author": "Odoo Italian Community, Agile Business Group, "
    "Odoo Community Association (OCA), TAKOBI",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": ["account_receipt_journal"],
    "data": [
        "views/partner_views.xml",
        "views/account_fiscal_position_views.xml",
    ],
    "installable": True,
    "pre_init_hook": "rename_old_italian_module",
}
