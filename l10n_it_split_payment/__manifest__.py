# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2018  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group.
# Copyright 2018  Ruben Tonetto (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Scissione pagamenti",
    "version": "14.0.1.0.6",
    "category": "Localization/Italy",
    "summary": "Scissione pagamenti",
    "author": "Abstract, Agile Business Group, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/account_view.xml",
        "views/config_view.xml",
    ],
    "images": [
        "static/fiscal_position.png",
        "static/settings.png",
        "static/SP.png",
        "static/SP2.png",
    ],
    "installable": True,
}
