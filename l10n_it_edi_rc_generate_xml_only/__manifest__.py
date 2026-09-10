# Copyright 2026 Marco Colombo <marco.colombo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italy EDI - Generate XML Only",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "development_status": "Alpha",
    "summary": "Generate FatturaPA XML for self-invoices without sending to SdI",
    "author": "Marco Colombo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["l10n_it_edi"],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
