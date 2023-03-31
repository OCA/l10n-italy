# © 2017 Alessandro Camilli - Openforce
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)
# Copyright 2021 Alex Comba - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "ITA - Codici carica",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Aggiunge la tabella dei codici carica da usare nelle dichiarazioni"
    " fiscali italiane",
    "author": "Openforce di Camilli Alessandro, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "data/appointment_code_data.xml",
        "views/appointment_code_view.xml",
    ],
    "installable": True,
}
