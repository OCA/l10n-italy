# Copyright 2026 Marco Colombo (<https://github/TheMule71)
# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Account Date Warning",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Show a warning when the accounting date is before the bill date",
    "author": "Marco Colombo <info@phi.technology>, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
